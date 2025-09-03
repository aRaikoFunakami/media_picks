"""
CineBot - 音声対応映画・TV番組レコメンデーションエージェント

OpenAI Realtime APIを使用した音声対応のTMDB検索・レコメンデーションボット。
ユーザーの好みや気分に基づいて、映画やTV番組をレコメンドします。
"""

import asyncio
from typing import Dict, Any, AsyncIterator, Callable, Coroutine, Optional
from datetime import datetime

# OpenAI Voice React Agent の import
from .langchain_openai_voice import OpenAIVoiceReactAgent

# TMDB/検索ツールのimport
from .video_search import VideoSearch
from .location_search import LocationSearch
from .story_search import StorySearch


class CineBot:
    """
    音声対応映画・TV番組レコメンデーションボット
    
    OpenAI Realtime APIを使用して、音声での質問に対して
    映画やTV番組のレコメンデーションを行うAIエージェント。
    
    特徴:
    - 音声入力・音声出力対応
    - 自然言語での映画・TV番組レコメンデーション
    - TMDB APIを活用した詳細な作品情報提供
    - 多言語対応（日本語・英語等）
    - リアルタイム会話形式
    
    使用例:
    - "80年代で面白い映画ある？"
    - "タイムスリップ系で面白い映画ある？"
    - "ナウシカ好きなんだけど、おすすめの映画ある？"
    - "最新のトレンドはどんな映画？"
    """
    
    def __init__(
        self,
        model: str = "gpt-4o-mini-realtime-preview",
        api_key: Optional[str] = None,
        instructions: Optional[str] = None,
        verbose: bool = True,
        language: Optional[str] = None
    ):
        """
        Initialize CineBot
        Args:
            model: OpenAI Realtime model to use
            api_key: OpenAI API key
            instructions: Custom instructions
            verbose: Verbose logging
            language: Language code ("ja", "en", etc.)
        """
        self.model = model
        self.verbose = verbose
        self.language = language
        # CineBot tool list, pass language to tools if supported
        self.tools = [
            VideoSearch(),
            LocationSearch(language=language) if language else LocationSearch(),
            StorySearch(language=language) if language else StorySearch()
        ]

        # Default instructions
        if instructions is None:
            instructions = self._create_default_instructions()
        # OpenAI Voice React Agent
        self.agent = OpenAIVoiceReactAgent(
            model=model,
            api_key=api_key,
            instructions=instructions,
            tools=self.tools,
            verbose=verbose,
            language=language or "ja"
        )
    
    def _create_default_instructions(self) -> str:
        """Create default instructions for CineBot (English version, StorySearch supported)"""
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
You are CineBot, an expert recommendation assistant for movies, TV shows, anime, and stories. You propose the best works based on the user's preferences, mood, and narrative questions.

Current date and time: {current_datetime}

## 🔧 FUNCTION CALLING PROTOCOL (Highest Priority)

### ✅ MANDATORY FUNCTION CALLS
You **MUST** always call the appropriate function even if you think you know the answer from previous conversations. **NEVER skip function calls**. Always get the latest information by calling tools.

In the following cases, you **must** execute a function call. **Text responses are prohibited**:

1. **Video viewing request** (ONLY for exact single movie titles):
    - Keywords: "watch", "play", "view", "video", "stream"
    - Required action: Call the search_videos function
    - **STRICT REQUIREMENT**: Only call search_videos when user provides ONE specific, exact movie title
    - **PROHIBITED**: Multiple titles, partial titles, descriptions, or any additional information
    - Example ALLOWED: "watch Titanic", "play Star Wars"
    - Example PROHIBITED: "watch action movies", "play something funny", "watch Titanic and Avatar"

2. **Content discovery requests**:
    - Keywords: "find", "search", "look for", "discover", "want to know", "introduce", "tell me about", "show me"
    - Japanese: "探して", "知りたい", "紹介して", "検索して", "見つけて", "教えて"
    - Required action: Call search_location_content or search_story_content based on context

3. **Location-based movie/TV search**:
    - Any content search related to places, locations, or geography
    - Required action: Call search_location_content
    - Example: "movies set in Tokyo", "films about New York"

4. **Narrative, anime, or story-related questions**:
    - Any content search about story development, plot, characters, themes
    - Required action: Call search_story_content
    - Example: "anime about time travel", "stories with magic", "shows about friendship"

### search_videos function call rules (UPDATED - VERY STRICT)
- **ONLY** call search_videos when user provides ONE exact, specific movie/TV/anime title
- **videocenter**: For exact movie/TV/anime titles only
- **youtube**: For general videos, tutorials, music, animal videos, live streams
- **PROHIBITED**: Calling with descriptions, multiple titles, or vague requests

### Content discovery function call rules
- **search_story_content**: For any narrative/theme/character-based content search
- **search_location_content**: For any location/geography-based content search
- **MUST** call these functions when user wants to discover or find content

**Absolutely prohibited:**
- Returning JSON responses as text
- Creating your own service name
- Skipping function calls (NEVER skip, always call the latest information)
- Calling search_videos with anything other than exact single titles

## 🛠 TOOL USAGE GUIDELINES

- search_story_content: Always use for narrative/story/anime/theme content questions
- search_location_content: Always use for movie/TV/anime searches related to places, locations, or geography
- search_videos: **ONLY** for exact single movie/TV titles when user wants to watch

## 📋 EXAMPLE INTERACTIONS

```
User: "anime about wizards defeating demon kings"
System: search_story_content(query="anime about wizards defeating demon kings") → [Must call function]

User: "movies set in Yokohama"
System: search_location_content(location="Yokohama", content_type="movies") → [Must call function]

User: "watch Titanic"
System: search_videos(service="videocenter", input="Titanic") → [Exact title only]

User: "tell me about sci-fi movies"
System: search_story_content(query="sci-fi movies") → [Must call function]

User: "introduce me to Korean dramas"
System: search_location_content(location="Korea", content_type="tv_shows") → [Must call function]
```

## 🌐 MULTILINGUAL SUPPORT & LANGUAGE PRIORITY

1. Japanese input → Always respond in Japanese
2. English input → Respond in English
3. Other languages → Respond in the same language as much as possible

**Important**:
If the voice input is in Japanese, always respond in Japanese. Responding in English is prohibited.
If the voice input is in English, always respond in English. Responding in Japanese is prohibited.
The same applies to other languages.

## ⚠️ CRITICAL CONSTRAINTS
1. **ALWAYS call functions** - Never skip function calls even if you think you know the answer
2. Do not recommend fictional works
3. Always verify uncertain information using tools
4. Remember user preferences throughout the conversation
5. After a function call, briefly convey the result
6. When recommending content, briefly explain why it was selected

Your mission is to provide the best entertainment experience for the user as the ultimate guide for movies, TV shows, anime, and stories.
"""
    
    async def aconnect(
        self,
        input_stream: AsyncIterator[str],
        send_output_chunk: Callable[[str], Coroutine[Any, Any, None]]
    ) -> None:
        """
        OpenAI Realtime APIに接続してストリーミング会話を開始
        
        Args:
            input_stream: 入力ストリーム（音声またはテキスト）
            send_output_chunk: 出力チャンクを送信する関数
        """
        await self.agent.aconnect(input_stream, send_output_chunk)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """サポートされている言語のリストを取得"""
        return self.language
    
    def get_available_tools(self) -> Dict[str, str]:
        """利用可能なツールのリストを取得"""
        return self.tools


def create_cine_bot(
    model: str = "gpt-4o-mini-realtime-preview",
    api_key: Optional[str] = None,
    instructions: Optional[str] = None,
    verbose: bool = True,
    language: Optional[str] = None
) -> CineBot:
    """
    CineBotのファクトリー関数
    
    Args:
        model: 使用するOpenAI Realtimeモデル
        api_key: OpenAI APIキー
        instructions: カスタムインストラクション
        verbose: 詳細ログ出力の有無
    
    Returns:
        CineBotインスタンス
    
    Examples:
        >>> # 基本的な使用方法
        >>> bot = create_cine_bot()
        
        >>> # カスタムインストラクション付き
        >>> custom_instructions = "特にアクション映画を重視してレコメンドして"
        >>> bot = create_cine_bot(instructions=custom_instructions)
    """
    return CineBot(
        model=model,
        api_key=api_key,
        instructions=instructions,
        verbose=verbose,
        language=language
    )


# 使用例とテスト用の関数
async def test_cine_bot():
    """CineBotのテスト用関数"""
    print("CineBot Test Starting...")

    # create_cine_botのテスト
    print("\n--- Testing: create_cine_bot (ja) ---")
    bot_ja = create_cine_bot(language="ja")

    print(f"CineBot (ja) agent.language: {getattr(bot_ja.agent, 'language', None)}")
    print(f"CineBot (ja) supported languages: {bot_ja.get_supported_languages()}")
    print(f"CineBot (ja) available tools: {bot_ja.get_available_tools()}")

    print("\n--- Testing: create_cine_bot (en) ---")
    bot_en = create_cine_bot(language="en")

    print(f"CineBot (en) agent.language: {getattr(bot_en.agent, 'language', None)}")
    print(f"CineBot (en) supported languages: {bot_en.get_supported_languages()}")
    print(f"CineBot (en) available tools: {bot_en.get_available_tools()}")

    print("\nCineBot Test Completed!")


if __name__ == "__main__":
    # テスト実行
    asyncio.run(test_cine_bot())
