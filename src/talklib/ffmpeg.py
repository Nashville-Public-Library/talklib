import ffmpeg

class FFMPEG:
    def __init__(self, 
                input_file: str = None,
                output_file: str = None,
                breakaway: int|float = 0,
                compression_level: int|float = 21,
                sample_rate: int = 44100,
                audio_channels: int = 1
                 ):

        self.input_file = input_file
        self.output_file = output_file
        self.breakaway = breakaway
        self.compression_level = compression_level
        self.sample_rate = sample_rate
        self.audio_channels = audio_channels

    def __build_input_commands(self) -> dict:
        command = {}
        command.update({'hide_banner': None})
        command.update({'loglevel': 'quiet'})
        command.update({'filename': self.input_file})

        return command
    
    def __build_output_commands(self) -> dict:
        command = {}
        command.update({'ar': self.sample_rate})
        command.update({'ac': self.audio_channels})
        command.update({'af': f'loudnorm=I=-{self.compression_level}'})
        if self.breakaway:
            command.update({'t': self.breakaway})
        command.update({'y': None})
        command.update({'filename': self.output_file})

        return command
    
    def get_commands(self):
        input_commands = self.__build_input_commands()
        output_commands = self.__build_output_commands()
        stream = ffmpeg.input(**input_commands)
        stream = ffmpeg.output(stream, **output_commands)
        ffmpeg_commands = ffmpeg.get_args(stream)
        return ffmpeg_commands

    def convert(self):
        '''convert file with ffmpeg and return filename'''
        input_commands = self.__build_input_commands()
        output_commands = self.__build_output_commands()
        stream = ffmpeg.input(**input_commands)
        stream = ffmpeg.output(stream, **output_commands)
        ffmpeg.run(stream, capture_stdout=True)
        return self.output_file
    
    def get_length_in_minutes(self) -> float:
        duration = ffmpeg.probe(filename=self.input_file)
        duration = duration['format']['duration']
        
        # convert the number to something more usable/readable
        duration = float(duration)
        duration = duration/60
        duration = round(duration, 2)

        return duration