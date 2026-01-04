"""
Offline Lichess-like Chess Application
Main entry point - with notation scheme support
"""
import sys
import pygame
import chess
import json
from pathlib import Path
from typing import Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
import subprocess
import time

# Constants
SQUARE_SIZE = 80
BOARD_SIZE = 8
WINDOW_SIZE = SQUARE_SIZE * BOARD_SIZE
MIN_WINDOW_SIZE = 320  # Minimum pencere boyutu

class InputMode(Enum):
    NONE = 0
    DRAGGING = 1
    CLICK_SELECT = 2

class NotationScheme(Enum):
    """Chess notation schemes"""
    ALGEBRAIC = "algebraic"  # Standard: e4, Nf3, etc.
    DESCRIPTIVE = "descriptive"  # Old: P-K4, N-KB3, etc.
    ICCF = "iccf"  # Numeric: 5254, 7163, etc.
    COORDINATE = "coordinate"  # Full coordinates: e2e4, g1f3, etc.
    FEN = "fen"  # Full board position in FEN format

@dataclass
class Arrow:
    start: Tuple[int, int]
    end: Tuple[int, int]

@dataclass
class Marker:
    square: Tuple[int, int]

class Config:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.load()
    
    def load(self):
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = self.get_defaults()
            self.save(data)
        
        self.animation_speed = data.get('animation_speed', 0.2)
        self.stockfish_path = data.get('stockfish_path', '/usr/bin/stockfish')
        self.stockfish_depth = data.get('stockfish_depth', 1)
        self.stockfish_time = data.get('stockfish_time', 0.001)
        
        self.arrow_color = tuple(data.get('arrow_color', [255, 0, 0]))
        self.arrow_thickness = data.get('arrow_thickness', 15)
        self.circle_color = tuple(data.get('circle_color', [70, 115, 80]))
        self.circle_thickness = data.get('circle_thickness', 4)
        self.circle_radius_ratio = data.get('circle_radius_ratio', 0.15)
        
        self.marker_color = tuple(data.get('marker_color', [255, 0, 0]))
        self.marker_thickness = data.get('marker_thickness', 4)
        self.marker_radius_ratio = data.get('marker_radius_ratio', 0.9)
        
        self.last_move_from_color = tuple(data.get('last_move_from_color', [205, 210, 106]))
        self.last_move_to_color = tuple(data.get('last_move_to_color', [170, 162, 58]))
        
        self.board_theme = data.get('board_theme', 'brown')
        self.piece_theme = data.get('piece_theme', 'cburnett')
        self.play_sounds = data.get('play_sounds', True)
        
        # Notation scheme setting
        notation = data.get('notation_scheme', 'algebraic')
        try:
            self.notation_scheme = NotationScheme(notation)
        except ValueError:
            self.notation_scheme = NotationScheme.ALGEBRAIC
        
        # Starting position FEN
        self.starting_fen = data.get('starting_fen', 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    
    def get_defaults(self):
        return {
            'animation_speed': 0.2,
            'stockfish_path': '/usr/bin/stockfish',
            'stockfish_depth': 1,
            'stockfish_time': 0.001,
            'arrow_color': [255, 0, 0],
            'arrow_thickness': 15,
            'circle_color': [70, 115, 80],
            'circle_thickness': 4,
            'circle_radius_ratio': 0.15,
            'marker_color': [255, 0, 0],
            'marker_thickness': 4,
            'marker_radius_ratio': 0.9,
            'last_move_from_color': [205, 210, 106],
            'last_move_to_color': [170, 162, 58],
            'board_theme': 'brown',
            'piece_theme': 'cburnett',
            'play_sounds': True,
            'notation_scheme': 'algebraic',
            'starting_fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        }
    
    def save(self, data):
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=2)

class NotationConverter:
    """Convert moves between different notation schemes"""
    
    @staticmethod
    def to_algebraic(move: chess.Move, board: chess.Board) -> str:
        """Convert to standard algebraic notation (SAN)"""
        return board.san(move)
    
    @staticmethod
    def to_coordinate(move: chess.Move) -> str:
        """Convert to coordinate notation (e.g., e2e4)"""
        return move.uci()
    
    @staticmethod
    def to_iccf(move: chess.Move) -> str:
        """Convert to ICCF numeric notation"""
        from_file = chess.square_file(move.from_square) + 1
        from_rank = chess.square_rank(move.from_square) + 1
        to_file = chess.square_file(move.to_square) + 1
        to_rank = chess.square_rank(move.to_square) + 1
        
        notation = f"{from_file}{from_rank}{to_file}{to_rank}"
        
        # Add promotion piece number if applicable
        if move.promotion:
            promo_map = {
                chess.QUEEN: '1',
                chess.ROOK: '2',
                chess.BISHOP: '3',
                chess.KNIGHT: '4'
            }
            notation += promo_map.get(move.promotion, '1')
        
        return notation
    
    @staticmethod
    def to_descriptive(move: chess.Move, board: chess.Board) -> str:
        """Convert to descriptive notation (old English style)"""
        piece = board.piece_at(move.from_square)
        if not piece:
            return move.uci()
        
        from_file = chess.square_file(move.from_square)
        from_rank = chess.square_rank(move.from_square)
        to_file = chess.square_file(move.to_square)
        to_rank = chess.square_rank(move.to_square)
        
        # Piece symbols in descriptive notation
        piece_map = {
            chess.PAWN: 'P',
            chess.KNIGHT: 'N',
            chess.BISHOP: 'B',
            chess.ROOK: 'R',
            chess.QUEEN: 'Q',
            chess.KING: 'K'
        }
        
        # File names in descriptive notation (from white's perspective)
        file_map = {
            0: 'QR', 1: 'QN', 2: 'QB', 3: 'Q',
            4: 'K', 5: 'KB', 6: 'KN', 7: 'KR'
        }
        
        piece_symbol = piece_map.get(piece.piece_type, 'P')
        
        # Adjust rank for black pieces
        if piece.color == chess.BLACK:
            display_rank = 8 - to_rank
        else:
            display_rank = to_rank + 1
        
        file_name = file_map.get(to_file, 'K')
        
        # Determine if capture
        is_capture = board.is_capture(move)
        separator = 'x' if is_capture else '-'
        
        notation = f"{piece_symbol}{separator}{file_name}{display_rank}"
        
        # Add special notations
        if board.is_castling(move):
            if to_file > from_file:
                return "O-O"
            else:
                return "O-O-O"
        
        if move.promotion:
            notation += f"={piece_map.get(move.promotion, 'Q')}"
        
        return notation
    
    @staticmethod
    def to_fen(board: chess.Board) -> str:
        """Convert current board position to FEN notation"""
        return board.fen()

class StockfishEngine:
    def __init__(self, path: str, depth: int = 15, time_limit: float = 1.0):
        self.process = subprocess.Popen(
            [path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        self.depth = depth
        self.time_limit = time_limit
        self._send('uci')
        self._wait_for('uciok')
        self._send('isready')
        self._wait_for('readyok')
    
    def _send(self, command: str):
        self.process.stdin.write(command + '\n')
        self.process.stdin.flush()
    
    def _wait_for(self, text: str):
        while True:
            line = self.process.stdout.readline().strip()
            if text in line:
                break
    
    def get_best_move(self, board: chess.Board) -> Optional[chess.Move]:
        self._send(f'position fen {board.fen()}')
        self._send(f'go depth {self.depth} movetime {int(self.time_limit * 1000)}')
        
        best_move = None
        while True:
            line = self.process.stdout.readline().strip()
            if line.startswith('bestmove'):
                move_str = line.split()[1]
                best_move = chess.Move.from_uci(move_str)
                break
        
        return best_move
    
    def close(self):
        self._send('quit')
        self.process.terminate()

class AssetManager:
    def __init__(self, config: Config):
        self.config = config
        self.assets_dir = Path('assets')
        self.pieces_dir = self.assets_dir / 'pieces' / config.piece_theme
        self.sounds_dir = self.assets_dir / 'sounds'
        self.boards_dir = self.assets_dir / 'boards'
        
        self.pieces = {}
        self.sounds = {}
        self.board_image = None
        self.check_image = None
        
        self._ensure_directories()
        self._load_pieces()
        self._load_sounds()
        self._load_board_theme()
        self._load_check_indicator()
    
    def _ensure_directories(self):
        self.assets_dir.mkdir(exist_ok=True)
        self.pieces_dir.mkdir(parents=True, exist_ok=True)
        self.sounds_dir.mkdir(parents=True, exist_ok=True)
        self.boards_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_pieces(self):
        piece_types = ['P', 'N', 'B', 'R', 'Q', 'K']
        colors = ['w', 'b']
        
        for color in colors:
            for piece in piece_types:
                key = f"{color}{piece}"
                png_path = self.pieces_dir / f"{key}.png"
                
                if png_path.exists():
                    self.pieces[key] = pygame.image.load(str(png_path))
    
    def _load_sounds(self):
        sound_files = {
            'Move': 'move',
            'Capture': 'capture',
            'Castle': 'castle',
            'Check': 'check',
            'Promote': 'promote',
            'GameEnd': 'end',
            'GenericNotify': 'notify'
        }
        
        for filename, key in sound_files.items():
            for ext in ['.ogg', '.mp3', '.wav']:
                filepath = self.sounds_dir / f"{filename}{ext}"
                if filepath.exists():
                    try:
                        self.sounds[key] = pygame.mixer.Sound(str(filepath))
                        break
                    except:
                        continue
    
    def _load_board_theme(self):
        board_path = self.boards_dir / f"{self.config.board_theme}.png"
        
        if board_path.exists():
            self.board_image = pygame.image.load(str(board_path))
    
    def _load_check_indicator(self):
        check_path = self.assets_dir / 'check.png'
        
        if check_path.exists():
            self.check_image = pygame.image.load(str(check_path))
    
    def get_piece_image(self, piece: chess.Piece, size: Tuple[int, int]) -> Optional[pygame.Surface]:
        """Get piece image scaled to (width, height) tuple"""
        color = 'w' if piece.color == chess.WHITE else 'b'
        piece_type = piece.symbol().upper()
        key = f"{color}{piece_type}"
        
        if key in self.pieces:
            return pygame.transform.smoothscale(self.pieces[key], size)
        
        # Fallback: render text
        avg_size = (size[0] + size[1]) // 2
        font = pygame.font.Font(None, avg_size)
        symbols = {'P': '♙♟', 'N': '♘♞', 'B': '♗♝', 'R': '♖♜', 'Q': '♕♛', 'K': '♔♚'}
        symbol = symbols[piece_type][0 if piece.color == chess.WHITE else 1]
        text = font.render(symbol, True, (255, 255, 255) if piece.color == chess.WHITE else (0, 0, 0))
        return text
    
    def get_board_surface(self, width: int, height: int) -> pygame.Surface:
        """Get board surface scaled to given width and height"""
        if self.board_image:
            return pygame.transform.smoothscale(self.board_image, (width, height))
        
        # Fallback: solid colors (brown theme) - rectangular squares
        surface = pygame.Surface((width, height))
        sq_w = width // 8
        sq_h = height // 8
        light = (240, 217, 181)
        dark = (181, 136, 99)
        
        for rank in range(8):
            for file in range(8):
                color = light if (file + rank) % 2 == 1 else dark
                pygame.draw.rect(surface, color, (file * sq_w, rank * sq_h, sq_w, sq_h))
        
        return surface
    
    def get_check_indicator(self, width: int, height: int) -> Optional[pygame.Surface]:
        """Get check indicator scaled to square size (width x height)"""
        if self.check_image:
            return pygame.transform.smoothscale(self.check_image, (width, height))
        return None
    
    def play_sound(self, sound_name: str):
        if self.config.play_sounds and sound_name in self.sounds:
            self.sounds[sound_name].play()

class ChessUI:
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize board with starting FEN from config
        self.board = chess.Board(config.starting_fen)
        
        # Initialize pygame first
        pygame.init()
        pygame.mixer.init()
        
        # Now load assets (which need mixer initialized)
        self.assets = AssetManager(config)
        
        # Initialize engine
        self.engine = StockfishEngine(
            config.stockfish_path,
            config.stockfish_depth,
            config.stockfish_time
        )
        
        self.window_size = WINDOW_SIZE
        
        # Create resizable window - can be rectangular
        self.window_width = self.window_size
        self.window_height = self.window_size
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height),
            pygame.RESIZABLE
        )
        pygame.display.set_caption('Offline Chess')
        
        self.clock = pygame.time.Clock()
        
        # Selection and move indicators - use circle_color from config
        self.selected_color = tuple(list(config.circle_color) + [128])  # Semi-transparent green
        self.legal_move_color = config.circle_color
        
        # Calculate lighter capture indicator color (30% lighter)
        self.capture_color = tuple(min(255, int(c * 1.3)) for c in config.circle_color)
        
        # Input state
        self.selected_square = None
        self.dragging_piece = None
        self.dragging_from_square = None
        self.drag_pos = None
        self.input_mode = InputMode.NONE
        
        # Arrow drawing state
        self.arrow_start = None
        
        # Markers and arrows
        self.arrows: List[Arrow] = []
        self.markers: List[Marker] = []
        
        # Last move highlighting
        self.last_move_from = None
        self.last_move_to = None
        
        # Animation (only for click-click moves)
        self.animating = False
        self.anim_start_time = 0
        self.anim_start_pos = None
        self.anim_end_pos = None
        self.anim_piece = None
        
        # Multi-animation queue for undo
        self.anim_queue = []
        self.current_anim_index = 0
        self.anim_board_states = []  # Store board states for each animation
        
        # Move history for undo
        self.move_history = []
        
        self.running = True
        self.player_color = chess.WHITE
        self.flipped = False  # Board orientation
    
    def square_size(self) -> Tuple[int, int]:
        """Calculate square width and height based on window dimensions"""
        square_width = self.window_width // BOARD_SIZE
        square_height = self.window_height // BOARD_SIZE
        return (square_width, square_height)
    
    def board_offset_x(self) -> int:
        """Calculate X offset - no offset needed now"""
        return 0
    
    def board_offset_y(self) -> int:
        """Calculate Y offset - no offset needed now"""
        return 0
    
    def get_square_from_pos(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        x, y = pos
        sq_w, sq_h = self.square_size()
        
        if 0 <= x < self.window_width and 0 <= y < self.window_height:
            file = x // sq_w
            rank = 7 - (y // sq_h)
            
            # Flip board if playing as black
            if self.flipped:
                file = 7 - file
                rank = 7 - rank
            
            return (file, rank)
        return None
    
    def square_to_pos(self, square: Tuple[int, int]) -> Tuple[int, int]:
        file, rank = square
        
        # Flip board if playing as black
        if self.flipped:
            file = 7 - file
            rank = 7 - rank
        
        sq_w, sq_h = self.square_size()
        
        x = file * sq_w
        y = (7 - rank) * sq_h
        return (x, y)
    
    def format_move(self, move: chess.Move, board: chess.Board) -> str:
        """Format move according to configured notation scheme"""
        scheme = self.config.notation_scheme
        
        if scheme == NotationScheme.ALGEBRAIC:
            return NotationConverter.to_algebraic(move, board)
        elif scheme == NotationScheme.COORDINATE:
            return NotationConverter.to_coordinate(move)
        elif scheme == NotationScheme.ICCF:
            return NotationConverter.to_iccf(move)
        elif scheme == NotationScheme.DESCRIPTIVE:
            return NotationConverter.to_descriptive(move, board)
        elif scheme == NotationScheme.FEN:
            # For FEN, we'll show the move in algebraic first, then the resulting FEN
            move_str = NotationConverter.to_algebraic(move, board)
            return move_str  # FEN will be printed separately
        else:
            return NotationConverter.to_algebraic(move, board)
    
    def draw_board(self):
        # Draw board theme - full window size
        board_surface = self.assets.get_board_surface(self.window_width, self.window_height)
        self.screen.blit(board_surface, (0, 0))
        
        # Draw last move highlighting
        if self.last_move_from and self.last_move_to:
            sq_w, sq_h = self.square_size()
            
            # Draw "from" square (lighter yellow)
            from_x, from_y = self.square_to_pos(self.last_move_from)
            from_highlight = pygame.Surface((sq_w, sq_h), pygame.SRCALPHA)
            from_color = self.config.last_move_from_color + (180,)  # Add alpha
            from_highlight.fill(from_color)
            self.screen.blit(from_highlight, (from_x, from_y))
            
            # Draw "to" square (darker yellow - 30% darker)
            to_x, to_y = self.square_to_pos(self.last_move_to)
            to_highlight = pygame.Surface((sq_w, sq_h), pygame.SRCALPHA)
            to_color = self.config.last_move_to_color + (180,)  # Add alpha
            to_highlight.fill(to_color)
            self.screen.blit(to_highlight, (to_x, to_y))
        
        # Draw check indicator if king is in check
        if self.board.is_check():
            king_square = self.board.king(self.board.turn)
            if king_square is not None:
                king_file = chess.square_file(king_square)
                king_rank = chess.square_rank(king_square)
                
                sq_w, sq_h = self.square_size()
                x, y = self.square_to_pos((king_file, king_rank))
                
                check_indicator = self.assets.get_check_indicator(sq_w, sq_h)
                if check_indicator:
                    self.screen.blit(check_indicator, (x, y))
        
        # Draw selection highlight (Lichess yellow)
        if self.selected_square:
            sq_w, sq_h = self.square_size()
            x, y = self.square_to_pos(self.selected_square)
            
            highlight = pygame.Surface((sq_w, sq_h), pygame.SRCALPHA)
            highlight.fill(self.selected_color)
            self.screen.blit(highlight, (x, y))
    
    def draw_legal_moves(self):
        if self.selected_square:
            sq = chess.square(self.selected_square[0], self.selected_square[1])
            piece = self.board.piece_at(sq)
            
            if piece and piece.color == self.board.turn:
                sq_w, sq_h = self.square_size()
                
                for move in self.board.legal_moves:
                    if move.from_square == sq:
                        to_file = chess.square_file(move.to_square)
                        to_rank = chess.square_rank(move.to_square)
                        x, y = self.square_to_pos((to_file, to_rank))
                        
                        # Create semi-transparent surface for indicators
                        indicator = pygame.Surface((sq_w, sq_h), pygame.SRCALPHA)
                        
                        if self.board.piece_at(move.to_square):
                            # Capture indicator (ring around edge)
                            color_with_alpha = tuple(list(self.capture_color) + [180])
                            # Draw ellipse ring
                            outer_rect = pygame.Rect(3, 3, sq_w - 6, sq_h - 6)
                            pygame.draw.ellipse(indicator, color_with_alpha, outer_rect, self.config.circle_thickness)
                        else:
                            # Move indicator (filled ellipse with configurable ratio)
                            dot_w = int(sq_w * self.config.circle_radius_ratio * 2)
                            dot_h = int(sq_h * self.config.circle_radius_ratio * 2)
                            dot_x = (sq_w - dot_w) // 2
                            dot_y = (sq_h - dot_h) // 2
                            
                            color_with_alpha = tuple(list(self.legal_move_color) + [180])
                            dot_rect = pygame.Rect(dot_x, dot_y, dot_w, dot_h)
                            pygame.draw.ellipse(indicator, color_with_alpha, dot_rect)
                        
                        self.screen.blit(indicator, (x, y))
    
    def draw_pieces(self):
        sq_w, sq_h = self.square_size()
        
        # Determine which board state to use for drawing
        current_board = self.board
        if self.anim_queue and self.current_anim_index < len(self.anim_board_states):
            current_board = self.anim_board_states[self.current_anim_index]
        
        for square in chess.SQUARES:
            piece = current_board.piece_at(square)
            if piece:
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                
                # Skip piece being dragged
                if self.dragging_piece and (file, rank) == self.dragging_from_square:
                    continue
                
                # Skip piece being animated (single animation)
                if self.animating and self.anim_piece and (file, rank) == self.anim_end_pos:
                    continue
                
                # Skip pieces being animated in queue (undo animations)
                # Only skip the CURRENT animation, not future ones
                if self.anim_queue and self.current_anim_index < len(self.anim_queue):
                    anim = self.anim_queue[self.current_anim_index]
                    # Skip piece at both start and end positions ONLY for current animation
                    if (file, rank) == anim['start_pos'] or (file, rank) == anim['end_pos']:
                        continue
                
                x, y = self.square_to_pos((file, rank))
                # Scale piece to fit rectangular square
                piece_size = (int(sq_w * 0.9), int(sq_h * 0.9))
                piece_img = self.assets.get_piece_image(piece, piece_size)
                
                if piece_img:
                    offset_x = (sq_w - piece_img.get_width()) // 2
                    offset_y = (sq_h - piece_img.get_height()) // 2
                    self.screen.blit(piece_img, (x + offset_x, y + offset_y))
    
    def draw_dragging_piece(self):
        if self.dragging_piece and self.drag_pos:
            sq_w, sq_h = self.square_size()
            piece_size = (int(sq_w * 0.9), int(sq_h * 0.9))
            piece_img = self.assets.get_piece_image(self.dragging_piece, piece_size)
            
            if piece_img:
                x = self.drag_pos[0] - piece_img.get_width() // 2
                y = self.drag_pos[1] - piece_img.get_height() // 2
                self.screen.blit(piece_img, (x, y))
    
    def draw_animating_piece(self):
        # Handle animation queue
        if self.anim_queue:
            if self.current_anim_index < len(self.anim_queue):
                anim = self.anim_queue[self.current_anim_index]
                elapsed = time.time() - anim['start_time']
                progress = min(elapsed / self.config.animation_speed, 1.0)
                
                sq_w, sq_h = self.square_size()
                start_x, start_y = self.square_to_pos(anim['start_pos'])
                end_x, end_y = self.square_to_pos(anim['end_pos'])
                
                current_x = start_x + (end_x - start_x) * progress
                current_y = start_y + (end_y - start_y) * progress
                
                piece_size = (int(sq_w * 0.9), int(sq_h * 0.9))
                piece_img = self.assets.get_piece_image(anim['piece'], piece_size)
                
                if piece_img:
                    offset_x = (sq_w - piece_img.get_width()) // 2
                    offset_y = (sq_h - piece_img.get_height()) // 2
                    self.screen.blit(piece_img, (current_x + offset_x, current_y + offset_y))
                
                if progress >= 1.0:
                    self.current_anim_index += 1
                    # Set start time for next animation
                    if self.current_anim_index < len(self.anim_queue):
                        self.anim_queue[self.current_anim_index]['start_time'] = time.time()
                    else:
                        self.anim_queue = []
                        self.anim_board_states = []
                        self.current_anim_index = 0
            
            self.animating = len(self.anim_queue) > 0
        
        # Handle single animation
        elif self.animating and self.anim_piece:
            elapsed = time.time() - self.anim_start_time
            progress = min(elapsed / self.config.animation_speed, 1.0)
            
            sq_w, sq_h = self.square_size()
            start_x, start_y = self.square_to_pos(self.anim_start_pos)
            end_x, end_y = self.square_to_pos(self.anim_end_pos)
            
            current_x = start_x + (end_x - start_x) * progress
            current_y = start_y + (end_y - start_y) * progress
            
            piece_size = (int(sq_w * 0.9), int(sq_h * 0.9))
            piece_img = self.assets.get_piece_image(self.anim_piece, piece_size)
            
            if piece_img:
                offset_x = (sq_w - piece_img.get_width()) // 2
                offset_y = (sq_h - piece_img.get_height()) // 2
                self.screen.blit(piece_img, (current_x + offset_x, current_y + offset_y))
            
            if progress >= 1.0:
                self.animating = False
    
    def draw_markers(self):
        sq_w, sq_h = self.square_size()
        
        for marker in self.markers:
            x, y = self.square_to_pos(marker.square)
            
            # Create rect for ellipse - use marker_radius_ratio for both dimensions
            marker_w = int(sq_w * self.config.marker_radius_ratio)
            marker_h = int(sq_h * self.config.marker_radius_ratio)
            
            # Center the ellipse in the square
            rect_x = x + (sq_w - marker_w) // 2
            rect_y = y + (sq_h - marker_h) // 2
            
            # Draw ellipse (oval) instead of circle
            rect = pygame.Rect(rect_x, rect_y, marker_w, marker_h)
            pygame.draw.ellipse(self.screen, self.config.marker_color, rect, self.config.marker_thickness)
    
    def draw_arrows(self):
        sq_w, sq_h = self.square_size()
        
        for arrow in self.arrows:
            start_x, start_y = self.square_to_pos(arrow.start)
            end_x, end_y = self.square_to_pos(arrow.end)
            
            start_center = (start_x + sq_w // 2, start_y + sq_h // 2)
            end_center = (end_x + sq_w // 2, end_y + sq_h // 2)
            
            # Draw line
            pygame.draw.line(self.screen, self.config.arrow_color,
                           start_center, end_center, self.config.arrow_thickness)
            
            # Draw arrowhead
            import math
            dx = end_center[0] - start_center[0]
            dy = end_center[1] - start_center[1]
            angle = math.atan2(dy, dx)
            
            avg_size = (sq_w + sq_h) // 2
            arrow_size = avg_size // 3
            left_angle = angle + 2.5
            right_angle = angle - 2.5
            
            left_x = end_center[0] - arrow_size * math.cos(left_angle)
            left_y = end_center[1] - arrow_size * math.sin(left_angle)
            right_x = end_center[0] - arrow_size * math.cos(right_angle)
            right_y = end_center[1] - arrow_size * math.sin(right_angle)
            
            pygame.draw.polygon(self.screen, self.config.arrow_color,
                              [end_center, (left_x, left_y), (right_x, right_y)])
    
    def clear_markers_and_arrows(self):
        self.markers.clear()
        self.arrows.clear()
    
    def animate_move(self, move: chess.Move):
        from_file = chess.square_file(move.from_square)
        from_rank = chess.square_rank(move.from_square)
        to_file = chess.square_file(move.to_square)
        to_rank = chess.square_rank(move.to_square)
        
        self.anim_start_pos = (from_file, from_rank)
        self.anim_end_pos = (to_file, to_rank)
        self.anim_piece = self.board.piece_at(move.from_square)
        self.anim_start_time = time.time()
        self.animating = True
    
    def make_move(self, move: chess.Move, animate: bool = True, record_history: bool = True):
        if animate:
            self.animate_move(move)
        
        is_capture = self.board.is_capture(move)
        is_castle = self.board.is_castling(move)
        is_check_before = self.board.is_check()
        
        # Store last move for highlighting
        from_file = chess.square_file(move.from_square)
        from_rank = chess.square_rank(move.from_square)
        to_file = chess.square_file(move.to_square)
        to_rank = chess.square_rank(move.to_square)
        
        self.last_move_from = (from_file, from_rank)
        self.last_move_to = (to_file, to_rank)
        
        # Record move in history
        if record_history:
            self.move_history.append(move)
        
        # Print move in configured notation with color prefix
        move_notation = self.format_move(move, self.board)
        
        # Determine which color made the move (before pushing)
        color_prefix = "White:" if self.board.turn == chess.WHITE else "Black:"
        
        # If using FEN notation, print both the move and resulting FEN
        if self.config.notation_scheme == NotationScheme.FEN:
            print(f"{color_prefix} {move_notation}")
            # Push the move first to get the resulting position
            self.board.push(move)
            fen = NotationConverter.to_fen(self.board)
            print(f"FEN: {fen}")
            # We already pushed, so don't push again below
            move_already_pushed = True
        else:
            print(f"{color_prefix} {move_notation}")
            move_already_pushed = False
        
        # Push move to board if not already done
        if not move_already_pushed:
            self.board.push(move)
        
        # Play sound
        if self.board.is_checkmate():
            self.assets.play_sound('end')
        elif self.board.is_check():
            self.assets.play_sound('check')
        elif move.promotion:
            self.assets.play_sound('promote')
        elif is_castle:
            self.assets.play_sound('castle')
        elif is_capture:
            self.assets.play_sound('capture')
        else:
            self.assets.play_sound('move')
    
    def handle_mouse_down(self, pos: Tuple[int, int], button: int):
        square = self.get_square_from_pos(pos)
        
        if button == 1:  # Left click
            # Clear markers and arrows when clicking
            self.clear_markers_and_arrows()
            
            if square:
                sq = chess.square(square[0], square[1])
                piece = self.board.piece_at(sq)
                
                # If clicking on own piece, either select it or start dragging
                if piece and piece.color == self.board.turn:
                    # If same piece clicked, deselect it
                    if self.selected_square == square:
                        self.selected_square = None
                    else:
                        # Select the piece
                        self.selected_square = square
                        self.input_mode = InputMode.CLICK_SELECT
                        
                        # Also start dragging in case user wants to drag
                        self.dragging_piece = piece
                        self.dragging_from_square = square
                        self.drag_pos = pos
                
                # If clicking on empty square or opponent piece while having selection
                elif self.selected_square:
                    # Try to make move (click-click mode with animation)
                    from_sq = chess.square(self.selected_square[0], self.selected_square[1])
                    to_sq = sq
                    move = chess.Move(from_sq, to_sq)
                    
                    # Check for promotion
                    if move in self.board.legal_moves:
                        self.make_move(move, animate=True)
                        self.selected_square = None
                    else:
                        # Try promotion
                        moved = False
                        for promo in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]:
                            promo_move = chess.Move(from_sq, to_sq, promotion=promo)
                            if promo_move in self.board.legal_moves:
                                self.make_move(promo_move, animate=True)
                                self.selected_square = None
                                moved = True
                                break
                        
                        # If invalid move, deselect
                        if not moved:
                            self.selected_square = None
                
                # Clicking on empty square with no selection - do nothing
                else:
                    self.selected_square = None
        
        elif button == 3:  # Right click
            if square:
                self.markers.append(Marker(square))
    
    def handle_mouse_up(self, pos: Tuple[int, int], button: int):
        if button == 1:
            square = self.get_square_from_pos(pos)
            
            # Handle drag-and-drop move (NO animation)
            if self.dragging_piece and self.dragging_from_square and self.drag_pos:
                # Check if actually dragged (moved cursor significantly)
                start_x, start_y = self.square_to_pos(self.dragging_from_square)
                sq_w, sq_h = self.square_size()
                start_center = (start_x + sq_w // 2, start_y + sq_h // 2)
                
                dx = abs(pos[0] - start_center[0])
                dy = abs(pos[1] - start_center[1])
                drag_threshold = min(sq_w, sq_h) // 4
                
                # If dragged significantly, make the move
                if (dx > drag_threshold or dy > drag_threshold) and square:
                    from_sq = chess.square(self.dragging_from_square[0], self.dragging_from_square[1])
                    to_sq = chess.square(square[0], square[1])
                    move = chess.Move(from_sq, to_sq)
                    
                    if move in self.board.legal_moves:
                        self.make_move(move, animate=False)  # NO animation for drag-drop
                        self.selected_square = None
                    else:
                        # Try promotion
                        for promo in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]:
                            promo_move = chess.Move(from_sq, to_sq, promotion=promo)
                            if promo_move in self.board.legal_moves:
                                self.make_move(promo_move, animate=False)  # NO animation
                                self.selected_square = None
                                break
                        else:
                            # Invalid move - piece stays selected for click-click mode
                            pass
                # If not dragged (just clicked), keep piece selected for click-click
                
                self.dragging_piece = None
                self.dragging_from_square = None
                self.drag_pos = None
                self.input_mode = InputMode.NONE
    
    def handle_mouse_motion(self, pos: Tuple[int, int]):
        if self.dragging_piece:
            self.drag_pos = pos
    
    def undo_move(self):
        """Undo last two moves (player + engine) with animation"""
        if not self.animating and len(self.move_history) >= 2:
            # Get last two moves
            engine_move = self.move_history.pop()
            player_move = self.move_history.pop()
            
            # Store board states for each animation step
            self.anim_board_states = []
            
            # Board state 1: Before undoing engine move (after both moves)
            board_state_1 = self.board.copy()
            self.anim_board_states.append(board_state_1)
            
            # Undo engine move
            self.board.pop()
            
            # Board state 2: After undoing engine move, before undoing player move
            board_state_2 = self.board.copy()
            self.anim_board_states.append(board_state_2)
            
            # Undo player move
            self.board.pop()
            
            # Create animation queue for both undos
            self.anim_queue = []
            
            # First animate engine move undo (reverse)
            engine_from_file = chess.square_file(engine_move.from_square)
            engine_from_rank = chess.square_rank(engine_move.from_square)
            engine_to_file = chess.square_file(engine_move.to_square)
            engine_to_rank = chess.square_rank(engine_move.to_square)
            
            # Get piece from the board state before undo
            engine_piece = board_state_1.piece_at(engine_move.to_square)
            
            self.anim_queue.append({
                'start_pos': (engine_to_file, engine_to_rank),
                'end_pos': (engine_from_file, engine_from_rank),
                'piece': engine_piece,
                'start_time': time.time()  # First animation starts immediately
            })
            
            # Then animate player move undo (reverse)
            player_from_file = chess.square_file(player_move.from_square)
            player_from_rank = chess.square_rank(player_move.from_square)
            player_to_file = chess.square_file(player_move.to_square)
            player_to_rank = chess.square_rank(player_move.to_square)
            
            # Get piece from the board state after undoing engine move
            player_piece = board_state_2.piece_at(player_move.to_square)
            
            self.anim_queue.append({
                'start_pos': (player_to_file, player_to_rank),
                'end_pos': (player_from_file, player_from_rank),
                'piece': player_piece,
                'start_time': 0  # Will be set when first animation completes
            })
            
            self.current_anim_index = 0
            self.animating = True
            
            # Clear last move highlight
            self.last_move_from = None
            self.last_move_to = None
            
            # Clear selection
            self.selected_square = None
    
    def reset_game(self):
        """Reset game to starting position from config"""
        self.board.set_fen(self.config.starting_fen)
        self.move_history.clear()
        self.last_move_from = None
        self.last_move_to = None
        self.selected_square = None
        self.clear_markers_and_arrows()
        self.animating = False
        self.anim_queue = []
        self.anim_board_states = []
    
    def flip_board(self):
        """Flip board orientation and switch player color"""
        self.flipped = not self.flipped
        self.player_color = chess.BLACK if self.player_color == chess.WHITE else chess.WHITE
        # Reset game when switching sides
        self.reset_game()
    
    def engine_move(self):
        if not self.board.is_game_over() and self.board.turn != self.player_color:
            move = self.engine.get_best_move(self.board)
            if move:
                self.make_move(move, animate=True)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.VIDEORESIZE:
                    # Simply update dimensions, don't call set_mode again
                    self.window_width = max(event.w, MIN_WINDOW_SIZE)
                    self.window_height = max(event.h, MIN_WINDOW_SIZE)
                
                elif event.type == pygame.KEYDOWN:
                    # Ctrl+Z: Undo
                    if event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL):
                        self.undo_move()
                    
                    # Ctrl+R: Reset game
                    elif event.key == pygame.K_r and (event.mod & pygame.KMOD_CTRL):
                        self.reset_game()
                    
                    # Ctrl+M: Flip board / Switch sides
                    elif event.key == pygame.K_m and (event.mod & pygame.KMOD_CTRL):
                        self.flip_board()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(event.pos, event.button)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(event.pos, event.button)
                
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
            
            # Draw
            self.draw_board()
            self.draw_legal_moves()
            self.draw_markers()
            self.draw_arrows()
            self.draw_pieces()
            self.draw_animating_piece()
            self.draw_dragging_piece()
            
            pygame.display.flip()
            self.clock.tick(60)
            
            # Engine move
            if not self.animating and not self.dragging_piece:
                self.engine_move()
        
        self.engine.close()
        pygame.quit()

def main():
    config = Config()
    ui = ChessUI(config)
    ui.run()

if __name__ == '__main__':
    main()