# sound_track.py
import arcade


class SoundTrack:
    def __init__(self):
        # Background noise
        self.background_noise = arcade.load_sound("assets/sounds/background_noise.wav")
        self.background_noise_playing = False
        self.background_noise_player = None
        self.background_noise_volume = 0.2
        # Load music tracks
        self.track1 = arcade.load_sound("assets/sounds/Billy's Sacrifice.wav")
        self.track2 = arcade.load_sound("assets/sounds/Checking Manifest.wav")
        self.track3 = arcade.load_sound("assets/sounds/Crash Landing.wav")
        self.track4 = arcade.load_sound("assets/sounds/Automatav2.wav")
        # Add more tracks as needed

        # Track duration in seconds
        self.track_durations = {
            self.track1: 234,
            self.track2: 240,
            self.track3: 217,
            self.track4: 246,
            # Add durations for more tracks as needed
        }

        # Track which song is currently playing and when it started
        self.current_track = None
        self.track_start_time = None

    def play_next_track(self, current_time):
        if self.current_track is None:
            self.current_track = self.track1
            self.track_start_time = current_time
            arcade.play_sound(self.track1, looping=False)
        elif self.current_track == self.track1 and (current_time - self.track_start_time) > self.track_durations[self.track1]:
            self.current_track = self.track2
            self.track_start_time = current_time
            arcade.play_sound(self.track2, looping=False)
        # ... Repeat for other tracks ...
        elif self.current_track == self.track4 and (current_time - self.track_start_time) > self.track_durations[self.track4]:
            self.current_track = self.track1
            self.track_start_time = current_time
            arcade.play_sound(self.track1, looping=False)

    def play_background_noise(self):
        if not self.background_noise_playing:
            self.background_noise_player = arcade.play_sound(self.background_noise, looping=True,
                                                             volume=self.background_noise_volume)
            self.background_noise_playing = True

    def stop_background_noise(self):
        if self.background_noise_playing:
            arcade.stop_sound(self.background_noise_player)
            self.background_noise_playing = False