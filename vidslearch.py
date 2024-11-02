import subprocess
import curses
from pytube import Search

def play_video(video_url):
    """Play video using MPV with optimized subprocess handling."""
    try:
        subprocess.run(['mpv', '--no-terminal', video_url], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing video: {e}")

def search_videos(query):
    """Search for videos"""
    search = Search(query)
    return search.results[:19]  # Results control

def display_ascii_art(stdscr):
    """Display ASCII header."""
    stdscr.addstr(0, 0, r"""
    //  $$\    $$\ $$\       $$\           $$\                                         $$\       $$\ $$\ $$\ 
    //  $$ |   $$ |\__|      $$ |          $$ |                                        $$ |      $$ |$$ |$$ |
    //  $$ |   $$ |$$\  $$$$$$$ | $$$$$$$\ $$ | $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$$\  $$ |$$ |$$ |
    //  \$$\  $$  |$$ |$$  __$$ |$$  _____|$$ |$$  __$$\  \____$$\ $$  __$$\ $$  _____|$$  __$$\ $$ |$$ |$$ |
    //   \$$\$$  / $$ |$$ /  $$ |\$$$$$$\  $$ |$$$$$$$$ | $$$$$$$ |$$ |  \__|$$ /      $$ |  $$ |\__|\__|\__|
    //    \$$$  /  $$ |$$ |  $$ | \____$$\ $$ |$$   ____|$$  __$$ |$$ |      $$ |      $$ |  $$ |            
    //     \$  /   $$ |\$$$$$$$ |$$$$$$$  |$$ |\$$$$$$$\ \$$$$$$$ |$$ |      \$$$$$$$\ $$ |  $$ |$$\ $$\ $$\ 
    //      \_/    \__| \_______|\_______/ \__| \_______| \_______|\__|       \_______|\__|  \__|\__|\__|\__|
    //                                                                
    //                                                                          - by florwithmriver0
    """)

def display_videos(stdscr, videos, current_selection):
    """Display the video list in a curses window."""
    stdscr.clear()
    display_ascii_art(stdscr)
    stdscr.addstr(11, 0, "Select a video to play (use arrow keys):")
    
    for idx, video in enumerate(videos):
        line = f"> {idx + 1}. {video.title}" if idx == current_selection else f"  {idx + 1}. {video.title}"
        stdscr.addstr(12 + idx, 0, line)
    
    stdscr.addstr(len(videos) + 12, 0, "Press 'q' to quit.")
    stdscr.refresh()

def main(stdscr):
    """Main function to handle the video player."""
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    stdscr.refresh()

    query = ""
    
    while True:
        stdscr.clear()
        display_ascii_art(stdscr)
        stdscr.addstr(10, 0, "Enter a search term (or 'exit' to quit):")
        stdscr.addstr(11, 0, query)
        stdscr.clrtoeol()
        stdscr.refresh()
        
        key = stdscr.getch()

        if key in (curses.KEY_BACKSPACE, 127):  # Handle backspace
            query = query[:-1]
        elif key == ord('\n'):  # Enter key to search
            if query.lower() == 'exit':
                break
            
            videos = search_videos(query)
            if not videos:
                stdscr.addstr(12, 0, "No videos found.")
                stdscr.refresh()
                stdscr.getch()
                query = ""  # Reset query
                continue
            
            current_selection = 0
            num_videos = len(videos)
            display_videos(stdscr, videos, current_selection)

            while True:
                key = stdscr.getch()

                if key == curses.KEY_UP and current_selection > 0:
                    current_selection -= 1
                elif key == curses.KEY_DOWN and current_selection < num_videos - 1:
                    current_selection += 1
                elif key == ord('\n'):  # Enter key to select a video
                    selected_video = videos[current_selection]
                    play_video(selected_video.watch_url)
                    stdscr.clear()
                    display_ascii_art(stdscr)
                    stdscr.addstr(0, 0, f"Playing: {selected_video.title}")
                    stdscr.refresh()
                    stdscr.getch()
                    break  # Exit to search again
                elif key == ord('q'):  # Quit the application
                    return

                display_videos(stdscr, videos, current_selection)

        else:
            if chr(key).isprintable():  # Only append printable characters
                query += chr(key)

if __name__ == "__main__":
    curses.wrapper(main)

