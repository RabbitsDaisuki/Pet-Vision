import time
import threading

class VideoPlayer:
    """
    Independent Video Player Module designed for asynchronous execution.
    """
    def __init__(self):
        self.is_playing = False

    def _play_logic(self, video_name):
        # Simulate a blocking playback process
        self.is_playing = True
        print(f"[Player] Initializing media: {video_name}")
        
        # Simulate video duration
        for second in range(1, 4):
            print(f"[Player] Playing... {second}s")
            time.sleep(1)
        
        print("[Player] Playback completed.")
        self.is_playing = False

    def trigger_play(self, video_name):
        """
        Creates a new thread to run the playback logic without blocking the caller.
        """
        if not self.is_playing:
            # Create a detached thread for video playback
            playback_thread = threading.Thread(
                target=self._play_logic, 
                args=(video_name,),
                daemon=True # Ensures the thread exits when the main program stops
            )
            playback_thread.start()
        else:
            print("[System Notice] Player is busy. Trigger ignored.")