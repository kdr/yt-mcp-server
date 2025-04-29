from typing import Any
import json
from pytube import extract
from mcp.server.fastmcp import FastMCP

## === Helpers ===

def normalize_youtube_url(url):
    """
    Normalize various YouTube URL formats to the canonical watch URL and extract the video ID.

    Parameters:
        url (str): The YouTube URL to normalize.

    Returns:
        tuple: A tuple containing the canonical URL and the video ID.
               Returns (None, None) if the video ID cannot be extracted.
    """
    try:
        video_id = extract.video_id(url)
        canonical_url = f'https://www.youtube.com/watch?v={video_id}'
        return canonical_url, video_id
    except Exception:
        return None, None
    
def get_youtube_thumbnail_url(video_id, quality='maxresdefault'):
    """
    Returns the thumbnail URL for a given YouTube video ID.

    Parameters:
        video_id (str): The YouTube video ID.
        quality (str): The desired thumbnail quality. Options include:
                       'default', 'mqdefault', 'hqdefault', 'sddefault', 'maxresdefault'.

    Returns:
        str: The URL of the thumbnail image.
    """
    return f'https://img.youtube.com/vi/{video_id}/{quality}.jpg'


def get_youtube_watch_url(video_id, start_time=None):
    """
    Returns the YouTube watch URL for a given video ID, optionally starting at a specific time.

    Parameters:
        video_id (str): The YouTube video ID.
        start_time (int or str, optional): The start time in seconds or in '1h2m3s' format.

    Returns:
        str: The YouTube watch URL.
    """
    base_url = f'https://www.youtube.com/watch?v={video_id}'
    if start_time is None:
        return base_url
    if isinstance(start_time, int):
        return f'{base_url}&t={start_time}s'
    else:
        return f'{base_url}&t={start_time}'


## === MCP Server ===

# Initialize FastMCP server
mcp = FastMCP("yt-mcp-server")

@mcp.tool()
async def get_watch_url(video_id: str, start_time: int = None) -> str:
    """Returns the YouTube watch URL for a given video ID, optionally starting at a specific time.

    Args:
        video_id: The YouTube video ID.
        start_time: The start time in seconds 
    """
    return json.dumps({
        "url": get_youtube_watch_url(video_id, start_time),
    })

@mcp.tool()
async def get_thumbnail_url(video_id: str) -> str:
    """Returns the thumbnail URL for a given YouTube video ID.

    Args:
        video_id: The YouTube video ID.
    """
    return json.dumps({
        "url": get_youtube_thumbnail_url(video_id),
    })

@mcp.tool()
async def get_normalized_url(url: str) -> str:
    """Returns the normalized YouTube URL for a given URL.

    Args:
        url: The YouTube URL to normalize.
    """
    return json.dumps({
        "url": normalize_youtube_url(url),
    })

## === Main ===

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
