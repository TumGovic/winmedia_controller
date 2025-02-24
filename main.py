import asyncio
import keyboard
from winrt.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus
)

class MediaController:
    def __init__(self):
        self.current_session = None
        self.media_info = None
        self.setup_hotkeys()

    def setup_hotkeys(self):
        keyboard.add_hotkey('play/pause media', self.toggle_playback)
        keyboard.add_hotkey('next track', self.next_track)
        keyboard.add_hotkey('previous track', self.previous_track)
        keyboard.add_hotkey('ctrl+alt+p', self.toggle_playback)

    async def get_media_session(self):
        sessions = await MediaManager.request_async()
        return sessions.get_current_session()

    async def update_media_info(self):
        session = await self.get_media_session()
        if not session:
            return None

        try:
            media_props = await session.try_get_media_properties_async()
            timeline = session.get_timeline_properties()
            playback_info = session.get_playback_info()

            # Основные свойства медиа
            media_info = {
                'title': media_props.title or "Unknown",
                'artist': media_props.artist or "Unknown",
                'album': media_props.album_title or "Unknown",
                'album_artist': media_props.album_artist or "Unknown",
                'track_id': media_props.track_number or 0,
                'genres': list(media_props.genres) if media_props.genres else [],
                'playback_type': playback_info.playback_type.name,
                'status': playback_info.playback_status.name,
                'position': timeline.position.total_seconds(),
                'duration': timeline.end_time.total_seconds(),
                'min_seek': timeline.min_seek_time.total_seconds(),
                'max_seek': timeline.max_seek_time.total_seconds(),
            }

            # Рассчет процента воспроизведения
            if media_info['duration'] > 0:
                media_info['progress_percent'] = (media_info['position'] / media_info['duration']) * 100
            else:
                media_info['progress_percent'] = 0

            self.media_info = media_info
        except Exception as e:
            print(f"Ошибка получения информации: {e}")
            return None
            
        return self.media_info

    async def toggle_playback(self):
        session = await self.get_media_session()
        if session:
            try:
                if session.get_playback_info().playback_status == PlaybackStatus.PLAYING:
                    await session.try_pause_async()
                else:
                    await session.try_play_async()
            except Exception as e:
                print(f"Ошибка управления воспроизведением: {e}")

    async def next_track(self):
        session = await self.get_media_session()
        if session:
            try:
                await session.try_skip_next_async()
            except Exception as e:
                print(f"Ошибка переключения трека: {e}")

    async def previous_track(self):
        session = await self.get_media_session()
        if session:
            try:
                await session.try_skip_previous_async()
            except Exception as e:
                print(f"Ошибка перехода к предыдущему треку: {e}")

    async def monitor(self):
        print("Медиа-контроллер запущен. Используйте медиа-клавиши для управления.")
        while True:
            try:
                info = await self.update_media_info()
                if info:
                    print("\n" + "="*50)
                    print(f"Трек: {info['artist']} - {info['title']}")
                    print(f"Альбом: {info['album']} (исполнитель: {info['album_artist']})")
                    print(f"Статус: {info['status']} ({info['playback_type']})")
                    print(f"Позиция: {info['position']:.1f} сек / {info['duration']:.1f} сек")
                    print(f"Прогресс: {info['progress_percent']:.2f}%")
                    print(f"ID трека: {info['track_id']}")
                    print(f"Жанры: {', '.join(info['genres'])}")
                    print(f"Доступная перемотка: {info['min_seek']:.1f}-{info['max_seek']:.1f} сек")
                else:
                    print("Нет активной медиа-сессии")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"Ошибка мониторинга: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    controller = MediaController()
    try:
        asyncio.run(controller.monitor())
    except KeyboardInterrupt:
        print("\nРабота скрипта завершена.")
        keyboard.unhook_all()