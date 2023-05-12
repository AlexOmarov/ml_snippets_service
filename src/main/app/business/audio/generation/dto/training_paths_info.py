from dataclasses import dataclass


@dataclass
class TrainingPathsInfo:
    metadata_file_path: str
    phonemes_file_path: str
    audio_files_dir_path: str
    checkpoint_path_template: str
    model_dir_path: str

    def serialize(self):
        return {
            'name': 'TrainingPathsInfo',
            'metadata_file_path': self.metadata_file_path,
            'audio_files_dir_path': self.audio_files_dir_path,
            'checkpoint_path_template': self.checkpoint_path_template,
            'phonemes_file_path': self.phonemes_file_path,
            'model_dir_path': self.model_dir_path,
        }