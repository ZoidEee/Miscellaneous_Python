# movie_database_logic.py

import os
import time

from pymediainfo import MediaInfo
from fractions import Fraction


class DirectoryViewerLogic:
    def __init__(self):
        self.recent_dirs = []

    def update_recent_dirs(self, dir_path):
        if dir_path not in self.recent_dirs:
            self.recent_dirs.insert(0, dir_path)
        if len(self.recent_dirs) > 5:
            self.recent_dirs.pop()

    def get_directory_info(self, dir_path):
        try:
            stat_info = os.stat(dir_path)
            total_size = 0
            file_count = 0
            subdir_count = 0
            for root, dirs, files in os.walk(dir_path):
                subdir_count += len(dirs)
                file_count += len(files)
                for f in files:
                    fp = os.path.join(root, f)
                    total_size += os.path.getsize(fp)
            return {
                'name': os.path.basename(dir_path),
                'created': time.ctime(stat_info.st_ctime),
                'modified': time.ctime(stat_info.st_mtime),
                'size': self.format_size(total_size),
                'subdirs': subdir_count,
                'files': file_count
            }
        except Exception as e:
            print(f"Error getting directory info: {str(e)}")
            return None

    def format_size(self, size):
        if size > 1e9:
            return f"{size / 1e9:.2f} GB"
        elif size > 1e6:
            return f"{size / 1e6:.2f} MB"
        else:
            return f"{size / 1e3:.2f} KB"

    def get_video_metadata(self, file_path):
        try:
            media_info = MediaInfo.parse(file_path)

            general_track = next((track for track in media_info.tracks if track.track_type == "General"), None)
            video_track = next((track for track in media_info.tracks if track.track_type == "Video"), None)
            audio_track = next((track for track in media_info.tracks if track.track_type == "Audio"), None)

            metadata = {
                'filename': os.path.basename(file_path),
                'size': self.format_size(os.path.getsize(file_path)),
            }

            if general_track:
                metadata.update({
                    'duration': general_track.duration / 1000 if general_track.duration else None,
                    'overall_bitrate': general_track.overall_bit_rate,
                })

            if video_track:
                metadata.update({
                    'video_format': video_track.format or video_track.codec,
                    'video_profile': video_track.codec_profile,
                    'width': video_track.width,
                    'height': video_track.height,
                    'fps': float(video_track.frame_rate) if video_track.frame_rate else None,
                    'bit_depth': video_track.bit_depth,
                    'pixel_format': video_track.pixel_format,
                    'video_bitrate': video_track.bit_rate,
                    'aspect_ratio': video_track.display_aspect_ratio,
                })

            if audio_track:
                metadata.update({
                    'audio_format': audio_track.format or audio_track.codec,
                    'audio_profile': audio_track.format_profile,
                    'channels': audio_track.channel_s,
                    'sample_rate': audio_track.sampling_rate,
                    'bit_depth': audio_track.bit_depth,
                    'audio_bitrate': audio_track.bit_rate,
                })

            return metadata
        except Exception as e:
            print(f"Error extracting metadata from {file_path}: {str(e)}")
            return None

    def format_bitrate(self, bitrate):
        if bitrate is None:
            return "N/A"
        bitrate = int(bitrate)
        if bitrate > 1000000:
            return f"{bitrate / 1000000:.2f} Mbps"
        elif bitrate > 1000:
            return f"{bitrate / 1000:.2f} Kbps"
        else:
            return f"{bitrate} bps"

    def format_duration(self, duration_seconds):
        if duration_seconds is None:
            return "N/A"
        hours, remainder = divmod(int(duration_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

    def format_aspect_ratio(self, aspect_ratio):
        if aspect_ratio is None:
            return "N/A"
        try:
            fraction = Fraction(aspect_ratio).limit_denominator(1000)
            return f"{fraction.numerator}:{fraction.denominator}"
        except (ValueError, ZeroDivisionError):
            return aspect_ratio  # Return the original value if conversion fails
