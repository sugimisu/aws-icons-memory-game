import pygame
import random
import os
import sys

# 基本設定
CARD_SIZE = 64
CARD_MARGIN = 5
BASE_WINDOW_WIDTH = 800
BASE_WINDOW_HEIGHT = 600

# 難易度設定
DIFFICULTY = {
    "EASY": {"grid": 4, "pairs": 8},     # 4x4 (16枚のカード、8ペア)
    "NORMAL": {"grid": 6, "pairs": 18},  # 6x6 (36枚のカード、18ペア)
    "HARD": {"grid": 8, "pairs": 32}     # 8x8 (64枚のカード、32ペア)
}

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 180)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Card:
    def __init__(self, image_path, x, y, pair_id):
        self.image_path = image_path
        self.x = x
        self.y = y
        self.pair_id = pair_id
        self.is_flipped = False
        self.is_matched = False
        self.image = None
        self.rect = pygame.Rect(x, y, CARD_SIZE, CARD_SIZE)
        
    def load_image(self):
        """画像を読み込み、32x32から64x64にリサイズ"""
        try:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (CARD_SIZE, CARD_SIZE))
        except (pygame.error, TypeError):
            # 画像が読み込めない場合は色付きの四角形を作成
            self.image = pygame.Surface((CARD_SIZE, CARD_SIZE))
            colors = [RED, GREEN, BLUE, (255, 255, 0), (255, 0, 255), (0, 255, 255)]
            self.image.fill(colors[self.pair_id % len(colors)])
    
    def draw(self, screen, font):
        """カードを描画"""
        if self.is_matched:
            # マッチしたカードは薄く表示
            pygame.draw.rect(screen, LIGHT_GRAY, self.rect)
            if self.image:
                temp_image = self.image.copy()
                temp_image.set_alpha(100)
                screen.blit(temp_image, (self.x, self.y))
        elif self.is_flipped:
            # 表向きのカード
            pygame.draw.rect(screen, WHITE, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)
            if self.image:
                screen.blit(self.image, (self.x, self.y))
        else:
            # 裏向きのカード
            pygame.draw.rect(screen, BLUE, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)
            # "AWS"テキストを表示
            text = font.render("AWS", True, WHITE)
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

class MemoryGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT))
        pygame.display.set_caption("AWS Icons Memory Game")
        self.clock = pygame.time.Clock()
        
        # 日本語フォントを設定
        font_loaded = False
        
        # 1. ヒラギノ角ゴシックフォントファイルを試す
        try:
            self.font = pygame.font.Font("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 24)
            self.big_font = pygame.font.Font("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 48)
            self.medium_font = pygame.font.Font("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", 36)
            font_loaded = True
            print("ヒラギノ角ゴシックフォントを使用します")
        except:
            pass
        
        # 2. システムフォント（hiraginosans）を試す
        if not font_loaded:
            try:
                self.font = pygame.font.SysFont("hiraginosans", 24)
                self.big_font = pygame.font.SysFont("hiraginosans", 48)
                self.medium_font = pygame.font.SysFont("hiraginosans", 36)
                font_loaded = True
                print("ヒラギノサンズシステムフォントを使用します")
            except:
                pass
        
        # 3. システムフォント（hiraginokakugothicpro）を試す
        if not font_loaded:
            try:
                self.font = pygame.font.SysFont("hiraginokakugothicpro", 24)
                self.big_font = pygame.font.SysFont("hiraginokakugothicpro", 48)
                self.medium_font = pygame.font.SysFont("hiraginokakugothicpro", 36)
                font_loaded = True
                print("ヒラギノ角ゴシックプロシステムフォントを使用します")
            except:
                pass
        
        # 4. Arial Unicodeを試す
        if not font_loaded:
            try:
                self.font = pygame.font.SysFont("arialunicode", 24)
                self.big_font = pygame.font.SysFont("arialunicode", 48)
                self.medium_font = pygame.font.SysFont("arialunicode", 36)
                font_loaded = True
                print("Arial Unicodeフォントを使用します")
            except:
                pass
        
        # 5. 最後の手段：デフォルトフォント
        if not font_loaded:
            print("日本語フォントが見つかりません。デフォルトフォントを使用します。")
            self.font = pygame.font.Font(None, 24)
            self.big_font = pygame.font.Font(None, 48)
            self.medium_font = pygame.font.Font(None, 36)
        
        # ゲーム状態
        self.state = "menu"  # "menu", "game", "game_over"
        self.difficulty = None
        self.grid_size = 0
        self.pairs_count = 0
        self.window_width = 0
        self.window_height = 0
        
        self.cards = []
        self.flipped_cards = []
        self.matches = 0
        self.attempts = 0
        
        # アイコンパスを取得
        self.icon_paths = self.get_icon_paths()
        
        # 難易度選択ボタン
        button_width = 200
        button_height = 60
        button_margin = 30
        start_y = BASE_WINDOW_HEIGHT // 2 - button_height
        
        self.difficulty_buttons = {
            "EASY": Button(
                BASE_WINDOW_WIDTH // 2 - button_width // 2,
                start_y,
                button_width, button_height,
                "かんたん (4×4)", GREEN, (100, 255, 100)
            ),
            "NORMAL": Button(
                BASE_WINDOW_WIDTH // 2 - button_width // 2,
                start_y + button_height + button_margin,
                button_width, button_height,
                "ふつう (6×6)", BLUE, (100, 100, 255)
            ),
            "HARD": Button(
                BASE_WINDOW_WIDTH // 2 - button_width // 2,
                start_y + 2 * (button_height + button_margin),
                button_width, button_height,
                "むずかしい (8×8)", RED, (255, 100, 100)
            )
        }
        
        # メニューに戻るボタン
        self.menu_button = Button(
            50, 50, 150, 40,
            "メニューに戻る", GRAY, LIGHT_GRAY
        )
        
    def get_icon_paths(self):
        """32pxのPNGアイコンパスを取得"""
        icon_paths = []
        base_path = "/Users/sugiyamamisuzu/pgame/awsicon"
        
        # findコマンドで32.pngファイルを検索
        import subprocess
        try:
            result = subprocess.run(
                ["find", base_path, "-name", "*32.png"],
                capture_output=True, text=True
            )
            paths = result.stdout.strip().split('\n')
            icon_paths = [path for path in paths if path and os.path.exists(path)]
        except:
            # findが使えない場合の代替手段
            print("アイコンの検索に失敗しました。代替カードを使用します。")
            icon_paths = []
        
        return icon_paths
    
    def setup_difficulty(self, difficulty):
        """難易度に応じてゲーム設定を行う"""
        self.difficulty = difficulty
        self.grid_size = DIFFICULTY[difficulty]["grid"]
        self.pairs_count = DIFFICULTY[difficulty]["pairs"]
        
        # ウィンドウサイズを計算
        self.window_width = self.grid_size * (CARD_SIZE + CARD_MARGIN) - CARD_MARGIN
        self.window_height = self.grid_size * (CARD_SIZE + CARD_MARGIN) - CARD_MARGIN + 100  # スコア表示用の余白
        
        # ウィンドウサイズが小さすぎる場合は最小サイズを設定
        self.window_width = max(self.window_width, 400)
        self.window_height = max(self.window_height, 400)
        
        # ウィンドウサイズを更新
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        
        # カードを初期化
        self.init_cards()
        
        # ゲーム状態をリセット
        self.matches = 0
        self.attempts = 0
        self.flipped_cards = []
        self.state = "game"
    
    def init_cards(self):
        """カードを初期化"""
        self.cards = []
        
        # 必要なアイコン数を計算
        needed_icons = min(self.pairs_count, len(self.icon_paths))
        
        # カードデータを作成
        card_data = []
        for i in range(self.pairs_count):
            if i < needed_icons:
                # 同じアイコンを2枚作成
                card_data.extend([self.icon_paths[i], self.icon_paths[i]])
            else:
                # アイコンが足りない場合は色付きカードを作成
                card_data.extend([None, None])
        
        # 奇数枚の場合、1枚余分に追加（ダミーカード）
        total_cards = self.grid_size * self.grid_size
        if len(card_data) < total_cards:
            card_data.append(None)
        
        # カードをシャッフル
        random.shuffle(card_data)
        
        # グリッドにカードを配置
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                index = row * self.grid_size + col
                if index < len(card_data):  # インデックスが範囲内かチェック
                    x = col * (CARD_SIZE + CARD_MARGIN)
                    y = row * (CARD_SIZE + CARD_MARGIN)
                    
                    card = Card(
                        card_data[index],
                        x, y,
                        index // 2  # ペアID
                    )
                    card.load_image()
                    self.cards.append(card)
    
    def handle_menu_click(self, pos, clicked):
        """メニュー画面でのクリックを処理"""
        for diff, button in self.difficulty_buttons.items():
            button.check_hover(pos)
            if clicked and button.is_clicked(pos, clicked):
                self.setup_difficulty(diff)
                return
    
    def handle_game_click(self, pos, clicked):
        """ゲーム画面でのクリックを処理"""
        # メニューボタンのチェック
        self.menu_button.check_hover(pos)
        if clicked and self.menu_button.is_clicked(pos, clicked):
            self.state = "menu"
            self.screen = pygame.display.set_mode((BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT))
            return
            
        # カードのクリック処理
        if not clicked or len(self.flipped_cards) >= 2:
            return
        
        for card in self.cards:
            if card.rect.collidepoint(pos) and not card.is_flipped and not card.is_matched:
                card.is_flipped = True
                self.flipped_cards.append(card)
                
                if len(self.flipped_cards) == 2:
                    self.check_match()
                break
    
    def check_match(self):
        """カードのマッチをチェック"""
        if len(self.flipped_cards) != 2:
            return
        
        card1, card2 = self.flipped_cards
        self.attempts += 1
        
        # 同じ画像パスかチェック
        if (card1.image_path == card2.image_path and card1.image_path is not None) or \
           (card1.image_path is None and card2.image_path is None and card1.pair_id == card2.pair_id):
            # マッチした場合
            card1.is_matched = True
            card2.is_matched = True
            self.matches += 1
            self.flipped_cards = []
            
            # ゲーム終了チェック
            if self.matches == self.pairs_count:
                self.state = "game_over"
        else:
            # マッチしなかった場合は少し待ってから裏返す
            pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # 1秒後
    
    def flip_back_cards(self):
        """マッチしなかったカードを裏返す"""
        for card in self.flipped_cards:
            card.is_flipped = False
        self.flipped_cards = []
    
    def draw_menu(self):
        """メニュー画面を描画"""
        self.screen.fill(WHITE)
        
        # タイトル
        title = self.big_font.render("AWS Icons Memory Game", True, BLACK)
        title_rect = title.get_rect(center=(BASE_WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # 説明
        subtitle = self.medium_font.render("難易度を選んでください", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(BASE_WINDOW_WIDTH // 2, 170))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 難易度ボタン
        for button in self.difficulty_buttons.values():
            button.draw(self.screen, self.font)
    
    def draw_game(self):
        """ゲーム画面を描画"""
        self.screen.fill(WHITE)
        
        # メニューボタン
        self.menu_button.draw(self.screen, self.font)
        
        # カードを描画
        for card in self.cards:
            card.draw(self.screen, self.font)
        
        # スコア表示
        score_y = self.grid_size * (CARD_SIZE + CARD_MARGIN)
        matches_text = self.font.render(f"マッチ: {self.matches}/{self.pairs_count}", True, BLACK)
        attempts_text = self.font.render(f"試行回数: {self.attempts}", True, BLACK)
        
        self.screen.blit(matches_text, (10, score_y + 10))
        self.screen.blit(attempts_text, (10, score_y + 35))
    
    def draw_game_over(self):
        """ゲーム終了画面を描画"""
        self.draw_game()  # ゲーム画面を描画
        
        # 半透明のオーバーレイ
        overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.screen.blit(overlay, (0, 0))
        
        # ゲームクリアメッセージ
        game_over_text = self.big_font.render("ゲームクリア！", True, GREEN)
        text_rect = game_over_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 30))
        self.screen.blit(game_over_text, text_rect)
        
        # スコア表示
        score_text = self.medium_font.render(f"試行回数: {self.attempts}", True, BLACK)
        score_rect = score_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        # 操作説明
        restart_text = self.font.render("Rキーでリスタート / Mキーでメニューに戻る", True, BLACK)
        restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        """状態に応じた画面を描画"""
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "game":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()
    
    def restart_game(self):
        """同じ難易度でゲームをリスタート"""
        self.setup_difficulty(self.difficulty)
    
    def run(self):
        """メインゲームループ"""
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左クリック
                        mouse_clicked = True
                        # 状態に応じたクリック処理
                        if self.state == "menu":
                            self.handle_menu_click(event.pos, True)
                        elif self.state == "game" or self.state == "game_over":
                            self.handle_game_click(event.pos, True)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.state == "game_over":
                        self.restart_game()
                    elif event.key == pygame.K_m and self.state == "game_over":
                        self.state = "menu"
                        self.screen = pygame.display.set_mode((BASE_WINDOW_WIDTH, BASE_WINDOW_HEIGHT))
                
                elif event.type == pygame.USEREVENT + 1:
                    # カードを裏返すタイマー
                    self.flip_back_cards()
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # タイマーを停止
            
            # マウスホバー処理（ボタンの見た目だけ変更）
            if self.state == "menu":
                for button in self.difficulty_buttons.values():
                    button.check_hover(mouse_pos)
            elif self.state == "game" or self.state == "game_over":
                self.menu_button.check_hover(mouse_pos)
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MemoryGame()
    game.run()
