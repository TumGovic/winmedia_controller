import asyncio
import keyboard
from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus
)

class MediaController:
    def __init__(self):
        self._setup_hotkeys()
    
    def _setup_hotkeys(self):
        keyboard.add_hotkey('play/pause media', self.toggle_playback)
        keyboard.add_hotkey('next track', self.next_track)
        keyboard.add_hotkey('previous track', self.previous_track)
    
    async def _get_session(self):
        sessions = await MediaManager.request_async()
        return sessions.get_current_session()
    
    async def get_media_info(self):
        session = await self._get_session()
        if not session:
            return None
        
        try:
            media_props = await session.try_get_media_properties_async()
            timeline = session.get_timeline_properties()
            playback_info = session.get_playback_info()
            
            return {
                'title': self._safe_str(media_props.title),
                'artist': self._safe_str(media_props.artist),
                'album': self._safe_str(media_props.album_title),
                'album_artist': self._safe_str(media_props.album_artist),
                'track_id': media_props.track_number or 0,
                'genres': list(media_props.genres) if media_props.genres else [],
                'status': playback_info.playback_status.name,
                'playback_type': playback_info.playback_type.name,
                'position': timeline.position.total_seconds(),
                'duration': timeline.end_time.total_seconds(),
                'progress_percent': self._calc_progress(
                    timeline.position.total_seconds(),
                    timeline.end_time.total_seconds()
                )
            }
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def _safe_str(self, value):
        return str(value) if value and str(value).strip() else "Unknown"
    
    def _calc_progress(self, pos, duration):
        return round((pos / duration * 100), 2) if duration > 0 else 0
    
    async def toggle_playback(self):
        session = await self._get_session()
        if session:
            try:
                if session.get_playback_info().playback_status == PlaybackStatus.PLAYING:
                    await session.try_pause_async()
                else:
                    await session.try_play_async()
            except Exception as e:
                print(f"Playback error: {str(e)}")
    
    async def next_track(self):
        session = await self._get_session()
        if session:
            try:
                await session.try_skip_next_async()
            except Exception as e:
                print(f"Next track error: {str(e)}")
    
    async def previous_track(self):
        session = await self._get_session()
        if session:
            try:
                await session.try_skip_previous_async()
            except Exception as e:
                print(f"Previous track error: {str(e)}")
    
    async def monitor(self, callback=None, interval=1):
        while True:
            info = await self.get_media_info()
            if callback and info:
                callback(info)
            await asyncio.sleep(interval)