import pygame
import sys
import os
import minimax

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)

class GameStateView:
    def __init__(self, minimax = None):
        self.images_viewed = set()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # pygame.display.set_caption("Image Viewer - Click Next to Navigate")
        self.clock = pygame.time.Clock()

        # Load images from a folder
        self.image_folder = "images"  # Change this to your image folder path
        self.images = self.load_images()
        self.current_image_index = 0

        # Font for text
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.minimax_result = None
        self.waiting_for_minimax = False
        self.status_text = "Ready"
        self.running = True
        self.minimax_tree = minimax

    def load_images(self):
        """Load all image files from the specified folder"""
        images = []
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

        # Create sample images if folder doesn't exist
        if not os.path.exists(self.image_folder):
            return self.create_sample_images()

        for filename in os.listdir(self.image_folder):
            if any(filename.lower().endswith(fmt) for fmt in supported_formats):
                image_path = os.path.join(self.image_folder, filename)
                try:
                    image = pygame.image.load(image_path)
                    images.append((image, filename))
                except pygame.error as e:
                    print(f"Could not load image {filename}: {e}")

        if not images:
            return self.create_sample_images()

        return images

    def create_sample_images(self):
        """Create sample colored rectangles as images"""
        colors = [
            ((255, 100, 100), "Red Image"),
            ((100, 255, 100), "Green Image"),
            ((100, 100, 255), "Blue Image"),
            ((255, 255, 100), "Yellow Image"),
            ((255, 100, 255), "Magenta Image")
        ]

        images = []
        for color, name in colors:
            surface = pygame.Surface((400, 300))
            surface.fill(color)
            # Add some text to make it more interesting
            text_surface = self.font.render(name, True, WHITE)
            text_rect = text_surface.get_rect(center=(200, 150))
            surface.blit(text_surface, text_rect)
            images.append((surface, name))

        return images

    def scale_image(self, image):
        """Scale image to fit screen while maintaining aspect ratio"""
        image_rect = image.get_rect()
        screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 80)  # Leave space for buttons

        # Calculate scaling factor
        scale_x = screen_rect.width / image_rect.width
        scale_y = screen_rect.height / image_rect.height
        scale = min(scale_x, scale_y, 1.0)  # Don't scale up

        new_width = int(image_rect.width * scale)
        new_height = int(image_rect.height * scale)

        return pygame.transform.scale(image, (new_width, new_height))

    def next_image(self):
        """Go to the next image"""
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.images_viewed.add(self.current_image_index)

            # If we've viewed all images, auto-exit
            if len(self.images_viewed) >= len(self.images):
                print(f"All {len(self.images)} images have been viewed. Auto-closing...")
                self.status_text = f"All {len(self.images)} images viewed! Closing in 2 seconds..."
                pygame.display.flip()
                pygame.time.wait(2000)  # Wait 2 seconds
                self.running = False

    def on_minimax_complete(self, result):
        """Called when minimax computation completes"""
        self.minimax_result = result
        # Automatically advance to next image
        self.next_image()

        self.status_text = f"Best move: {result}"
        self.waiting_for_minimax = False

        print(f"Minimax completed with result: {result}")

    def start_minimax(self):
        """Start minimax computation in background"""
        if self.minimax_tree and not self.waiting_for_minimax:
            self.waiting_for_minimax = True
            self.status_text = "Running Minimax..."

            self.minimax_tree.run(self)

    def draw_status(self):
        """Draw status information"""
        # Controls
        controls = [
            "ENTER: Run Minimax",
        ]

        for i, control in enumerate(controls):
            control_surface = self.small_font.render(control, True, BLACK)
            self.screen.blit(control_surface, (10, SCREEN_HEIGHT - 100 + i * 20))

        # Status text
        status_surface = self.small_font.render(f"Status: {self.status_text}", True, BLACK)
        self.screen.blit(status_surface, (10, 40))

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RETURN:
                    self.start_minimax()

    def update(self):
        """Update game state view"""
        self.handle_events()

    def draw(self):
        """Draw the current game state"""
        self.screen.fill(WHITE)

        # Draw current image
        if self.images:
            current_image, _ = self.images[self.current_image_index]
            scaled_image = self.scale_image(current_image)

            image_rect = scaled_image.get_rect()
            image_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT - 100) // 2 + 30)
            self.screen.blit(scaled_image, image_rect)

        # Draw status and controls
        self.draw_status()

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# Main execution
if __name__ == "__main__":
    viewer = GameStateView()
    viewer.run()

