"""
Simulación de Solitario Klondike
Juego de cartas implementado con Tkinter
Incluye animaciones, drag & drop, y lógica completa del juego
"""

import tkinter as tk
from tkinter import messagebox
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Constantes del juego
CARD_WIDTH = 70
CARD_HEIGHT = 95
CARD_SPACING = 20
PILE_SPACING = 10
SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
COLORS = {'♠': 'black', '♣': 'black', '♥': 'red', '♦': 'red'}

@dataclass
class Card:
    """Representa una carta del juego"""
    suit: str
    rank: str
    face_up: bool = False
    
    def get_value(self) -> int:
        """Retorna el valor numérico de la carta"""
        return RANKS.index(self.rank) + 1
    
    def get_color(self) -> str:
        """Retorna el color de la carta"""
        return COLORS[self.suit]
    
    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

class CardWidget:
    """Widget visual para una carta"""
    def __init__(self, canvas: tk.Canvas, card: Card, x: int, y: int):
        self.canvas = canvas
        self.card = card
        self.x = x
        self.y = y
        self.rect_id = None
        self.text_ids = []
        self.draw()
    
    def draw(self):
        """Dibuja la carta en el canvas"""
        # Eliminar dibujo anterior
        self.clear()
        
        # Dibujar rectángulo de la carta
        if self.card.face_up:
            fill = 'white'
            outline = 'black'
        else:
            fill = '#2E5090'
            outline = 'black'
        
        self.rect_id = self.canvas.create_rectangle(
            self.x, self.y,
            self.x + CARD_WIDTH, self.y + CARD_HEIGHT,
            fill=fill, outline=outline, width=2,
            tags=('card',)
        )
        
        # Dibujar contenido de la carta
        if self.card.face_up:
            color = self.card.get_color()
            # Símbolo superior izquierdo
            self.text_ids.append(
                self.canvas.create_text(
                    self.x + 8, self.y + 12,
                    text=f"{self.card.rank}\n{self.card.suit}",
                    fill=color, font=('Arial', 10, 'bold'),
                    tags=('card',)
                )
            )
            # Símbolo central grande
            self.text_ids.append(
                self.canvas.create_text(
                    self.x + CARD_WIDTH/2, self.y + CARD_HEIGHT/2,
                    text=self.card.suit,
                    fill=color, font=('Arial', 32, 'bold'),
                    tags=('card',)
                )
            )
        else:
            # Patrón para carta boca abajo
            pattern = "❖"
            self.text_ids.append(
                self.canvas.create_text(
                    self.x + CARD_WIDTH/2, self.y + CARD_HEIGHT/2,
                    text=pattern * 3 + '\n' + pattern * 3,
                    fill='white', font=('Arial', 14),
                    tags=('card',)
                )
            )
    
    def clear(self):
        """Elimina el dibujo de la carta"""
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        for text_id in self.text_ids:
            self.canvas.delete(text_id)
        self.text_ids = []
    
    def move_to(self, x: int, y: int, animate: bool = False):
        """Mueve la carta a una nueva posición"""
        if animate:
            # Animación suave
            steps = 10
            dx = (x - self.x) / steps
            dy = (y - self.y) / steps
            
            for _ in range(steps):
                self.x += dx
                self.y += dy
                self.draw()
                self.canvas.update()
                self.canvas.after(20)
        
        self.x = x
        self.y = y
        self.draw()

class SolitaireGame:
    """Clase principal del juego de Solitario"""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Solitario Klondike")
        self.root.resizable(False, False)
        
        # Canvas principal
        self.canvas = tk.Canvas(
            root, width=800, height=650,
            bg='#0B7F3F', highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Botones de control
        self.create_controls()
        
        # Estado del juego
        self.deck: List[Card] = []
        self.waste: List[Card] = []
        self.foundations: List[List[Card]] = [[] for _ in range(4)]
        self.tableau: List[List[Card]] = [[] for _ in range(7)]
        
        # Widgets visuales
        self.card_widgets: List[CardWidget] = []
        
        # Variables para drag & drop
        self.dragging = False
        self.drag_data = {'cards': [], 'source': None, 'start_x': 0, 'start_y': 0}
        
        # Vincular eventos
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)
        
        # Iniciar juego
        self.new_game()
    
    def create_controls(self):
        """Crea los botones de control"""
        control_frame = tk.Frame(self.root, bg='#0B7F3F')
        control_frame.pack(pady=5)
        
        tk.Button(
            control_frame, text="Nuevo Juego", command=self.new_game,
            font=('Arial', 12, 'bold'), bg='#FFA500', fg='white',
            padx=15, pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            control_frame, text="Reiniciar", command=self.restart_game,
            font=('Arial', 12, 'bold'), bg='#4169E1', fg='white',
            padx=15, pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        self.moves_label = tk.Label(
            control_frame, text="Movimientos: 0",
            font=('Arial', 12, 'bold'), bg='#0B7F3F', fg='white'
        )
        self.moves_label.pack(side=tk.LEFT, padx=20)
        
        self.moves = 0
    
    def new_game(self):
        """Inicia un nuevo juego"""
        # Crear y mezclar baraja
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        random.shuffle(self.deck)
        
        # Reiniciar pilas
        self.waste = []
        self.foundations = [[] for _ in range(4)]
        self.tableau = [[] for _ in range(7)]
        
        # Distribuir cartas en tableau
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.pop()
                if j == i:
                    card.face_up = True
                self.tableau[i].append(card)
        
        # Reiniciar movimientos
        self.moves = 0
        self.update_moves()
        
        # Redibujar todo
        self.redraw_all()
    
    def restart_game(self):
        """Reinicia el juego actual"""
        self.new_game()
    
    def redraw_all(self):
        """Redibuja todas las cartas"""
        # Limpiar canvas
        self.canvas.delete('all')
        self.card_widgets = []
        
        # Dibujar indicadores de posición
        self.draw_placeholders()
        
        # Dibujar mazo
        self.draw_deck()
        
        # Dibujar waste
        self.draw_waste()
        
        # Dibujar fundaciones
        self.draw_foundations()
        
        # Dibujar tableau
        self.draw_tableau()
    
    def draw_placeholders(self):
        """Dibuja los espacios vacíos para las pilas"""
        # Mazo y waste
        for i in range(2):
            x = 30 + i * (CARD_WIDTH + CARD_SPACING)
            self.canvas.create_rectangle(
                x, 30, x + CARD_WIDTH, 30 + CARD_HEIGHT,
                outline='white', width=2, dash=(5, 5)
            )
        
        # Fundaciones
        for i in range(4):
            x = 370 + i * (CARD_WIDTH + CARD_SPACING)
            self.canvas.create_rectangle(
                x, 30, x + CARD_WIDTH, 30 + CARD_HEIGHT,
                outline='white', width=2, dash=(5, 5)
            )
        
        # Tableau
        for i in range(7):
            x = 30 + i * (CARD_WIDTH + CARD_SPACING)
            self.canvas.create_rectangle(
                x, 170, x + CARD_WIDTH, 170 + CARD_HEIGHT,
                outline='white', width=2, dash=(5, 5)
            )
    
    def draw_deck(self):
        """Dibuja el mazo"""
        if self.deck:
            x, y = 30, 30
            card = self.deck[-1]
            widget = CardWidget(self.canvas, card, x, y)
            self.card_widgets.append(widget)
    
    def draw_waste(self):
        """Dibuja la pila de descarte"""
        if self.waste:
            x = 30 + CARD_WIDTH + CARD_SPACING
            y = 30
            # Mostrar hasta 3 cartas superpuestas
            for i, card in enumerate(self.waste[-3:]):
                offset = i * 20
                widget = CardWidget(self.canvas, card, x + offset, y)
                self.card_widgets.append(widget)
    
    def draw_foundations(self):
        """Dibuja las fundaciones"""
        for i, foundation in enumerate(self.foundations):
            x = 370 + i * (CARD_WIDTH + CARD_SPACING)
            y = 30
            if foundation:
                card = foundation[-1]
                widget = CardWidget(self.canvas, card, x, y)
                self.card_widgets.append(widget)
    
    def draw_tableau(self):
        """Dibuja el tableau"""
        for i, pile in enumerate(self.tableau):
            x = 30 + i * (CARD_WIDTH + CARD_SPACING)
            y = 170
            for j, card in enumerate(pile):
                offset = j * PILE_SPACING
                widget = CardWidget(self.canvas, card, x, y + offset)
                self.card_widgets.append(widget)
    
    def on_click(self, event):
        """Maneja el clic del mouse"""
        x, y = event.x, event.y
        
        # Verificar clic en mazo
        if self.is_click_on_deck(x, y):
            self.draw_from_deck()
            return
        
        # Verificar clic en waste
        clicked_waste = self.is_click_on_waste(x, y)
        if clicked_waste:
            self.start_drag_from_waste(x, y)
            return
        
        # Verificar clic en fundaciones
        foundation_idx = self.is_click_on_foundation(x, y)
        if foundation_idx is not None:
            self.start_drag_from_foundation(foundation_idx, x, y)
            return
        
        # Verificar clic en tableau
        pile_idx, card_idx = self.is_click_on_tableau(x, y)
        if pile_idx is not None:
            self.start_drag_from_tableau(pile_idx, card_idx, x, y)
            return
    
    def is_click_on_deck(self, x: int, y: int) -> bool:
        """Verifica si el clic fue en el mazo"""
        deck_x, deck_y = 30, 30
        return (deck_x <= x <= deck_x + CARD_WIDTH and
                deck_y <= y <= deck_y + CARD_HEIGHT)
    
    def is_click_on_waste(self, x: int, y: int) -> bool:
        """Verifica si el clic fue en waste"""
        if not self.waste:
            return False
        waste_x = 30 + CARD_WIDTH + CARD_SPACING
        waste_y = 30
        # Considerar las cartas superpuestas
        offset = min(len(self.waste) - 1, 2) * 20
        return (waste_x <= x <= waste_x + CARD_WIDTH + offset and
                waste_y <= y <= waste_y + CARD_HEIGHT)
    
    def is_click_on_foundation(self, x: int, y: int) -> Optional[int]:
        """Verifica si el clic fue en alguna fundación"""
        for i in range(4):
            fx = 370 + i * (CARD_WIDTH + CARD_SPACING)
            fy = 30
            if fx <= x <= fx + CARD_WIDTH and fy <= y <= fy + CARD_HEIGHT:
                return i
        return None
    
    def is_click_on_tableau(self, x: int, y: int) -> Tuple[Optional[int], Optional[int]]:
        """Verifica si el clic fue en alguna pila del tableau"""
        for i, pile in enumerate(self.tableau):
            tx = 30 + i * (CARD_WIDTH + CARD_SPACING)
            ty = 170
            
            for j, card in enumerate(pile):
                card_y = ty + j * PILE_SPACING
                if (tx <= x <= tx + CARD_WIDTH and
                    card_y <= y <= card_y + CARD_HEIGHT and
                    card.face_up):
                    return i, j
        return None, None
    
    def draw_from_deck(self):
        """Roba carta del mazo"""
        if self.deck:
            card = self.deck.pop()
            card.face_up = True
            self.waste.append(card)
            self.increment_moves()
        elif self.waste:
            # Reiniciar mazo desde waste
            while self.waste:
                card = self.waste.pop()
                card.face_up = False
                self.deck.append(card)
            self.increment_moves()
        
        self.redraw_all()
    
    def start_drag_from_waste(self, x: int, y: int):
        """Inicia arrastre desde waste"""
        if self.waste:
            self.dragging = True
            self.drag_data['cards'] = [self.waste[-1]]
            self.drag_data['source'] = 'waste'
            self.drag_data['start_x'] = x
            self.drag_data['start_y'] = y
    
    def start_drag_from_foundation(self, idx: int, x: int, y: int):
        """Inicia arrastre desde fundación"""
        if self.foundations[idx]:
            self.dragging = True
            self.drag_data['cards'] = [self.foundations[idx][-1]]
            self.drag_data['source'] = ('foundation', idx)
            self.drag_data['start_x'] = x
            self.drag_data['start_y'] = y
    
    def start_drag_from_tableau(self, pile_idx: int, card_idx: int, x: int, y: int):
        """Inicia arrastre desde tableau"""
        pile = self.tableau[pile_idx]
        if card_idx < len(pile) and pile[card_idx].face_up:
            self.dragging = True
            self.drag_data['cards'] = pile[card_idx:]
            self.drag_data['source'] = ('tableau', pile_idx)
            self.drag_data['start_x'] = x
            self.drag_data['start_y'] = y
    
    def on_drag(self, event):
        """Maneja el arrastre"""
        if self.dragging:
            # Aquí se podría implementar visualización del arrastre
            pass
    
    def on_release(self, event):
        """Maneja la liberación del mouse"""
        if not self.dragging:
            return
        
        x, y = event.x, event.y
        moved = False
        
        # Intentar mover a fundación
        foundation_idx = self.is_click_on_foundation(x, y)
        if foundation_idx is not None and len(self.drag_data['cards']) == 1:
            if self.can_move_to_foundation(self.drag_data['cards'][0], foundation_idx):
                self.move_to_foundation(foundation_idx)
                moved = True
        
        # Intentar mover a tableau
        if not moved:
            for i in range(7):
                tx = 30 + i * (CARD_WIDTH + CARD_SPACING)
                ty = 170
                pile_height = len(self.tableau[i]) * PILE_SPACING + CARD_HEIGHT
                
                if tx <= x <= tx + CARD_WIDTH and ty <= y <= ty + pile_height:
                    if self.can_move_to_tableau(self.drag_data['cards'], i):
                        self.move_to_tableau(i)
                        moved = True
                        break
        
        # Si no se movió, redibujar
        if not moved:
            self.redraw_all()
        
        # Reiniciar drag
        self.dragging = False
        self.drag_data = {'cards': [], 'source': None, 'start_x': 0, 'start_y': 0}
    
    def can_move_to_foundation(self, card: Card, foundation_idx: int) -> bool:
        """Verifica si una carta puede moverse a una fundación"""
        foundation = self.foundations[foundation_idx]
        
        if not foundation:
            return card.rank == 'A'
        
        top_card = foundation[-1]
        return (card.suit == top_card.suit and
                card.get_value() == top_card.get_value() + 1)
    
    def can_move_to_tableau(self, cards: List[Card], pile_idx: int) -> bool:
        """Verifica si cartas pueden moverse a una pila del tableau"""
        pile = self.tableau[pile_idx]
        first_card = cards[0]
        
        if not pile:
            return first_card.rank == 'K'
        
        top_card = pile[-1]
        return (first_card.get_color() != top_card.get_color() and
                first_card.get_value() == top_card.get_value() - 1)
    
    def move_to_foundation(self, foundation_idx: int):
        """Mueve carta a fundación"""
        card = self.drag_data['cards'][0]
        source = self.drag_data['source']
        
        # Remover de origen
        if source == 'waste':
            self.waste.pop()
        elif source[0] == 'foundation':
            self.foundations[source[1]].pop()
        elif source[0] == 'tableau':
            pile = self.tableau[source[1]]
            pile.pop()
            if pile and not pile[-1].face_up:
                pile[-1].face_up = True
        
        # Agregar a fundación
        self.foundations[foundation_idx].append(card)
        self.increment_moves()
        self.redraw_all()
        self.check_win()
    
    def move_to_tableau(self, pile_idx: int):
        """Mueve cartas a tableau"""
        cards = self.drag_data['cards']
        source = self.drag_data['source']
        
        # Remover de origen
        if source == 'waste':
            self.waste.pop()
        elif source[0] == 'foundation':
            self.foundations[source[1]].pop()
        elif source[0] == 'tableau':
            source_pile = self.tableau[source[1]]
            for _ in cards:
                source_pile.pop()
            if source_pile and not source_pile[-1].face_up:
                source_pile[-1].face_up = True
        
        # Agregar a destino
        self.tableau[pile_idx].extend(cards)
        self.increment_moves()
        self.redraw_all()
    
    def increment_moves(self):
        """Incrementa el contador de movimientos"""
        self.moves += 1
        self.update_moves()
    
    def update_moves(self):
        """Actualiza la etiqueta de movimientos"""
        self.moves_label.config(text=f"Movimientos: {self.moves}")
    
    def check_win(self):
        """Verifica si el jugador ha ganado"""
        if all(len(f) == 13 for f in self.foundations):
            messagebox.showinfo(
                "¡Felicitaciones!",
                f"¡Has ganado!\nMovimientos: {self.moves}"
            )

# Inicializar aplicación
if __name__ == '__main__':
    root = tk.Tk()
    game = SolitaireGame(root)
    root.mainloop()