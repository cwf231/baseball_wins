from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


class Stopwatch:
    """
    A simple stopwatch object.
    --------------------------
    
    Parameters:
    -----------
    auto_start: bool (default: True)
        Set whether to start the stopwatch when it's created.
        
    Attributes:
    -----------
    start_time: datetime object
        The recorded time the stopwatch started.
    times: list
        A list of tuples ('label', 'datetime_object') for each lap recorded.
        (Includes the start and stop times.)
    stop_time: datetime object
        The recorded time the stopwatch stopped.
            
    """
    def __init__(self, auto_start=True):
        self.start_time = None
        self.times = []
        self.stop_time = None
        
        if auto_start:
            self.start()
    
    def start(self, force_reset=True):
        """
        Start the stopwatch.
        --------------------
        
        Parameters:
        -----------
        force_reset: bool (default: True)
            If true, the stopwatch will reset all stored values back to their defaults before starting.
            If false and the timer has times logged, an exception will be raised.
        """
        if self.times and not force_reset:
            raise Exception('Please reset timer using .reset() or set force_reset=True.')
        if force_reset:
            self.reset()
        self.start_time = datetime.now()
        self.times.append(('Start', self.start_time))
        
    def lap(self, label=None):
        """
        Create a timestamp of a lap being completed.
        Appends the list of times in the stopwatch.
        The overall stopwatch continues running.
        --------------------------------------------
        
        Parameters:
        -----------
        label: str
            The label of the lap for identification and plotting purposes.
            If none is passed, the default 'Lap{n}' will be passed.
        """
        if not label:
            label = f'Lap{len(self.times)}'
        self.times.append((label, datetime.now()))
        
    def stop(self):
        """
        Stop the stopwatch.
        This will freeze all times in its times list.
        """
        if not self.start_time:
            print('Timer not started.')
            return
        self.stop_time = datetime.now()
        self.times.append(('Stop', self.stop_time))
        
    def reset(self):
        """
        Restore to factory settings.
        """
        self.__init__(auto_start=False)
        
        
    def elapsed_time_(self):
        """
        Returns the difference between the start_time and the stop_time.
        """
        if self.stop_time and self.start_time:
            elapsed = self.stop_time - self.start_time
            return elapsed
        
    def display_laps(self, 
                     figsize=(8,4), 
                     mark_elapsed_time=True,
                     show_stop=True,
                     annotate=True, 
                     verbose=True,
                     vlines=True,
                     styles=['ggplot', 'seaborn-talk']):
        """
        Plots the stored times - start_time, laps, stop_time.
        -----------------------------------------------------
        
        Parameters:
        -----------
        figsize: tup (default: (8, 4))
            Size of the output figure (width, height).
        mark_elapsed_time: bool (default: True)
            Calculate and plot the difference in time from each point to the starting point (0).
            If false, the points will be plotted on their datetime objects.
        annotate: bool (default: True)
            Label the points with their stored labels.
        verbose: bool (default: True)
            If true, display a dataframe with columns=[label, timestamp, [elapsed_time]].
        vlines: bool (default: True)
            Plot a dotted vertical line on each point in the times list.
        styles: list of strings (or string) (default: ['ggplot', 'seaborn-talk'])
            Desired style of plot. Must be compatible with matplotlib styles.
        """
        if not self.times:
            print('No times to display.')
            return
        
        if show_stop:
            times = self.times
        else:
            times = self.times[:-1]
        
        with plt.style.context(styles):
            fig, ax = plt.subplots(figsize=figsize)
            if mark_elapsed_time:
                x = [(x[1] - self.start_time).total_seconds() 
                     for x in times]
                ax.set(xlabel='Elapsed Time (sec)')
            else:
                x = [a[1] for a in times]
                ax.set(xlabel='Time Recorded')
            y = [0 for _ in x]

            ax.scatter(x=x, y=y)
            if annotate:
                [plt.annotate(label, 
                              (x[i], y[i]), 
                              xytext=(x[i], y[i]+0.005)) 
                 for i, (label, x_val) in enumerate(times)]
                
            if vlines:
                if mark_elapsed_time:
                    [ax.axvline(x_val, ls=':') for x_val in x]
                else:
                    [ax.axvline(i[1], ls=':') for i in times]
            
            ax.set_yticklabels([])
            ax.set_yticks([])
            fig.tight_layout()
        if verbose:
            df = pd.DataFrame(times, columns=['Label', 'Timestamp'])
            if mark_elapsed_time:
                df['Elapsed Time (sec)'] = x
            display(df)
        plt.show()