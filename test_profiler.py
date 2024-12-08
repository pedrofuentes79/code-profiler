from src.CodeProfiler import CodeProfiler
from src.DataFrameFactory import DataFrameFactory
from zoneinfo import ZoneInfo
from pytest import raises, mark
import pickle

ARG = ZoneInfo("America/Argentina/Buenos_Aires")
UTC = ZoneInfo("UTC")
generator = DataFrameFactory()

df = generator.generate_time_series_df("2024-01-01", 10, "min")
df_numeric = generator.generate_numeric_df_named('value', 10000)
gdf = generator.generate_random_gdf(num_polygons=10000, vertices=8, x_range=(0, 10), y_range=(0, 10))


@mark.skip('it is not reliably slower')
def test_profiler_chooses_correct_snippet():
    profiler = CodeProfiler()
    
    def pandas(df):
        df['msgTime'] = df['msgTime'].dt.tz_localize(ARG)
        return df
    def pydatetime(df):
        df['msgTime'] = df['msgTime'].apply(lambda date: date.to_pydatetime().astimezone(ARG))
        return df

    assert profiler.is_faster_than(pandas, pydatetime, df, verbose=False, num_iterations=10)

# @mark.skip
def test_profiler_raises_if_snippets_dont_return_same_result():
    profiler = CodeProfiler()

    def pydatetime(df):
        df['msgTime'] = df['msgTime'].apply(lambda date: date.to_pydatetime().astimezone(ARG))
        return df
    def pandas(df):
        df['msgTime'] = df['msgTime'].dt.tz_localize(UTC)
        return df

    with raises(ValueError):
        profiler.is_faster_than(pandas, pydatetime, df)

# @mark.skip
def test_profiler_chooses_correct_snippet_with_geometries():
    profiler = CodeProfiler()

    def apply(gdf):
        gdf['area'] = gdf['geometry'].apply(lambda geom: geom.area)
        return gdf
    def geopandas(gdf):
        gdf['area'] = gdf.area
        return gdf
        
    results_apply = profiler.results_from_func(apply, gdf)
    results_geopandas = profiler.results_from_func(geopandas, gdf)

    print(results_apply['execution_time'], results_geopandas['execution_time'])
    print(results_apply['memory_usage'], results_geopandas['memory_usage'])

    assert profiler.is_faster_than(geopandas, apply, gdf)

# @mark.skip
def test_profiler_chooses_correct_snippet_vectorized_operation():
    profiler = CodeProfiler()

    def efficient_sum(df):
        df['sum'] = df['value'].cumsum()
        return df
    
    def apply_sum(df):
        df['sum'] = [sum(df['value'][:i+1]) for i in range(len(df))]
        return df
    
    assert profiler.is_faster_than(efficient_sum, apply_sum, df_numeric, verbose=True)

# @mark.skip
def test_profiler_knows_which_snippet_uses_less_memory():
    profiler = CodeProfiler()

    def memory_efficient(df):
        df['doubled'] = df['value'] * 2
        return df
    
    def memory_inefficient(df):
        values = df['value'].values.tolist()
        doubled = [value * 2 for value in values]
        df['doubled'] = doubled.copy()
        return df
    
    assert profiler.is_more_memory_efficient_than(memory_efficient, memory_inefficient, df_numeric, verbose=True)


if __name__ == '__main__':
    test_profiler_chooses_correct_snippet()