import os
from scipy.io import wavfile
import numpy as np
from tqdm import tqdm
from datetime import datetime, timedelta
import json

class SilenceSplitter:

    def __init__(self, inputPath:str):
        self.InputPath = inputPath

    def split(self):
        files = os.listdir(self.InputPath)
        for fileNamer in files:
            os.remove(self.run_audioSeg(fileName=fileNamer))
        print("Silence Split Done")

#helper functions
    def GetTime(self, video_seconds):
        if (video_seconds < 0) :
            return 00
        else:
            sec = timedelta(seconds=float(video_seconds))
            d = datetime(1,1,1) + sec

            instant = str(d.hour).zfill(2) + ':' + str(d.minute).zfill(2) + ':' + str(d.second).zfill(2) + str('.001')
        
            return instant

    def energy(self,samples):
        return np.sum(np.power(samples, 2.)) / float(len(samples))
    
    def windows(self, signal, window_size, step_size):
        if type(window_size) is not int:
            raise AttributeError("Window size must be an integer.")
        if type(step_size) is not int:
            raise AttributeError("Step size must be an integer.")
        for i_start in range(0, len(signal), step_size):
            i_end = i_start + window_size
            if i_end >= len(signal):
                break
            yield signal[i_start:i_end]
        
    def rising_edges(self, binary_signal):
        previous_value = 0
        index = 0
        for x in binary_signal:
            if x and not previous_value:
                yield index
            previous_value = x
            index += 1

#segment/split the file
    def run_audioSeg(self, fileName:str):
        '''
        Last Acceptable Values

        min_silence_length = 0.3
        silence_threshold = 1e-3
        step_duration = 0.03/10

        '''
        input_file = os.path.join(self.InputPath,fileName).replace("\\","/")
        if not input_file:
            raise ValueError("No file selected.")
        output_dir = self.InputPath
        min_silence_length = 0.6
        silence_threshold = 1e-4
        step_duration = 0.03/10

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        input_filename = input_file
        window_duration = min_silence_length
        if step_duration is None:
            step_duration = window_duration / 10.
        else:
            step_duration = step_duration

        output_filename_prefix = os.path.splitext(os.path.basename(input_filename))[0]
        dry_run = False

        print("Splitting {} where energy is below {}% for longer than {}s.".format(
            input_filename,
            silence_threshold * 100.,
            window_duration
            )
        )

        # Read and split the file

        sample_rate, samples = input_data=wavfile.read(filename=input_filename, mmap=True)

        max_amplitude = np.iinfo(samples.dtype).max
        print(max_amplitude)

        max_energy = self.energy([max_amplitude])
        print(max_energy)

        window_size = int(window_duration * sample_rate)
        step_size = int(step_duration * sample_rate)

        signal_windows = self.windows(
            signal=samples,
            window_size=window_size,
            step_size=step_size
        )

        window_energy = (self.energy(w) / max_energy for w in tqdm(
            signal_windows,
            total=int(len(samples) / float(step_size))
        ))

        window_silence = (e > silence_threshold for e in window_energy)

        cut_times = (r * step_duration for r in self.rising_edges(window_silence))

        # This is the step that takes long, since we force the generators to run.
        print(" Finding silences...")
        cut_samples = [int(t * sample_rate) for t in cut_times]
        cut_samples.append(-1)

        cut_ranges = [(i, cut_samples[i], cut_samples[i+1]) for i in range(len(cut_samples) - 1)]

        video_sub = {str(i) : [str(self.GetTime(((cut_samples[i])/sample_rate))), 
                            str(self.GetTime(((cut_samples[i+1])/sample_rate)))] 
                    for i in range(len(cut_samples) - 1)}

        for i, start, stop in tqdm(cut_ranges):
            output_file_path = "{}_{:03d}.wav".format(
                os.path.join(output_dir, output_filename_prefix),
                i
            )
            if not dry_run:
                print("Writing file {}".format(output_file_path))
                wavfile.write(
                    filename=output_file_path,
                    rate=sample_rate,
                    data=samples[start:stop]
                )
            else:
                print("Not writing file {}".format(output_file_path))
        return input_file