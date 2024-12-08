from time import perf_counter as time_counter
from memory_profiler import memory_usage
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from src.constants import *

pd.options.mode.copy_on_write = True

class CodeProfiler:
    
    def results_from_func(self, func, data, metric=EXECUTION_TIME, verbose=False):
        """Metric and verbose are only used for printing purposes"""
        data_copy = data.copy(deep=False)
        mem_usage_before = memory_usage(-1, interval=0.1, timeout=1)[0]
        start_time = time_counter()
        result = func(data_copy)
        end_time = time_counter()
        mem_usage_after = memory_usage(-1, interval=0.1, timeout=1)[0]
        
        response = {
            RESULT: result,
            EXECUTION_TIME: end_time - start_time,
            MEMORY_USAGE: mem_usage_after - mem_usage_before,
        }
         
        if verbose:
            print(response[metric])
        return response

    def compare_functions(self, func1, func2, data, metric, num_iterations, verbose=False):
        results_1 = self.metrics_from(func1, data, num_iterations, metric, verbose)
        results_2 = self.metrics_from(func2, data, num_iterations, metric, verbose)
        
        self.assert_valid_results(results_1, results_2)

        return np.mean([res1[metric] for res1 in results_1]) < np.mean([res2[metric] for res2 in results_2])
  
    def metrics_from(self, func1, data, num_iterations, metric, verbose):
        return [self.results_from_func(func1, data, metric, verbose) for _ in range(num_iterations)]
 
    def is_more_memory_efficient_than(self, func1, func2, data, verbose=False, num_iterations=1):
        return self.compare_functions(func1, func2, data, MEMORY_USAGE, num_iterations, verbose)

    def is_faster_than(self, func1, func2, data, verbose=False, num_iterations=1):
        return self.compare_functions(func1, func2, data, EXECUTION_TIME, num_iterations, verbose)
    

    # region assertions

    def assert_valid_results(self, results1, results2):
        for res1, res2 in zip(results1, results2):
            if isinstance(res1['result'], (DataFrame, Series)):
                are_equal = self.dataframes_are_equal(res1['result'], res2['result'])
            else:
                are_equal = res1['result'] == res2['result']

            if not are_equal:
                print(res1['result'])
                print(res2['result'])
                raise ValueError(f"Results are not equal")

    def dataframes_are_equal(self, df1, df2):
        return df1.equals(df2)