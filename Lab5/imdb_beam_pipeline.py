import apache_beam as beam
import csv
import io

# ----- Helper Functions -----

def parse_csv(line):
    """Parse a single CSV line into a dictionary."""
    reader = csv.reader(io.StringIO(line))
    fields = next(reader)
    headers = [
        'name', 'rating', 'genre', 'year', 'released',
        'score', 'votes', 'director', 'writer', 'star',
        'country', 'budget', 'gross', 'company', 'runtime'
    ]
    if len(fields) != len(headers):
        return None
    return dict(zip(headers, fields))


def is_valid_record(record):
    """Filter out None records and header row."""
    if record is None:
        return False
    if record.get('name') == 'name':
        return False
    return True


def safe_float(value):
    """Safely convert a value to float, return None if invalid."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


# ----- Transform Functions -----

def extract_genre_score(record):
    """Extract (genre, score) pairs."""
    score = safe_float(record.get('score'))
    genre = record.get('genre', '').strip()
    if score is not None and genre:
        return [(genre, score)]
    return []


def extract_genre_count(record):
    """Extract (genre, 1) pairs for counting."""
    genre = record.get('genre', '').strip()
    if genre:
        return [(genre, 1)]
    return []


def extract_year_budget(record):
    """Extract (year, budget) pairs."""
    budget = safe_float(record.get('budget'))
    year = record.get('year', '').strip()
    if budget is not None and year and budget > 0:
        return [(year, budget)]
    return []


def extract_genre_gross(record):
    """Extract (genre, gross) pairs."""
    gross = safe_float(record.get('gross'))
    genre = record.get('genre', '').strip()
    if gross is not None and genre and gross > 0:
        return [(genre, gross)]
    return []


class AverageFn(beam.CombineFn):
    """Custom CombineFn to compute average."""
    def create_accumulator(self):
        return (0.0, 0)  # (sum, count)

    def add_input(self, accumulator, input_value):
        total, count = accumulator
        return (total + input_value, count + 1)

    def merge_accumulators(self, accumulators):
        totals, counts = zip(*accumulators)
        return (sum(totals), sum(counts))

    def extract_output(self, accumulator):
        total, count = accumulator
        return round(total / count, 2) if count > 0 else 0.0


def format_result(kv, label):
    """Format a key-value pair into a readable string."""
    return f'{label} | {kv[0]}: {kv[1]}'


# ----- Main Pipeline -----

def run():
    input_file = 'data/movies.csv'

    with beam.Pipeline() as pipeline:
        # Read and parse CSV
        records = (
            pipeline
            | 'ReadCSV' >> beam.io.ReadFromText(input_file)
            | 'ParseCSV' >> beam.Map(parse_csv)
            | 'FilterInvalid' >> beam.Filter(is_valid_record)
        )

        # 1. Average IMDb Score per Genre
        (
            records
            | 'ExtractGenreScore' >> beam.FlatMap(extract_genre_score)
            | 'AvgScorePerGenre' >> beam.CombinePerKey(AverageFn())
            | 'FormatAvgScore' >> beam.Map(format_result, 'AvgScore')
            | 'WriteAvgScore' >> beam.io.WriteToText(
                'outputs/avg_score_per_genre', file_name_suffix='.txt')
        )

        # 2. Movie Count per Genre
        (
            records
            | 'ExtractGenreCount' >> beam.FlatMap(extract_genre_count)
            | 'SumCountPerGenre' >> beam.CombinePerKey(sum)
            | 'FormatCount' >> beam.Map(format_result, 'MovieCount')
            | 'WriteCount' >> beam.io.WriteToText(
                'outputs/movie_count_per_genre', file_name_suffix='.txt')
        )

        # 3. Average Budget per Year
        (
            records
            | 'ExtractYearBudget' >> beam.FlatMap(extract_year_budget)
            | 'AvgBudgetPerYear' >> beam.CombinePerKey(AverageFn())
            | 'FormatBudget' >> beam.Map(format_result, 'AvgBudget')
            | 'WriteBudget' >> beam.io.WriteToText(
                'outputs/avg_budget_per_year', file_name_suffix='.txt')
        )

        # 4. Total Gross Revenue per Genre
        (
            records
            | 'ExtractGenreGross' >> beam.FlatMap(extract_genre_gross)
            | 'SumGrossPerGenre' >> beam.CombinePerKey(sum)
            | 'FormatGross' >> beam.Map(format_result, 'TotalGross')
            | 'WriteGross' >> beam.io.WriteToText(
                'outputs/total_gross_per_genre', file_name_suffix='.txt')
        )

    print("Pipeline completed! Check the 'outputs/' folder for results.")


if __name__ == '__main__':
    run()