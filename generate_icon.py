"""Generate a conic gradient ring icon for Ember High Contrast theme."""

from PIL import Image
import math

SIZE = 512
CENTER = SIZE // 2
PADDING = 40
RADIUS = SIZE // 2 - PADDING
RING_THICKNESS = 50  # width of the ring
INNER_RADIUS = RADIUS - RING_THICKNESS

# Theme accent colors evenly spaced around the circle.
# Last stop wraps back to the first color for a seamless loop.
COLORS = [
    (0 / 7, (233, 100, 1)),    # orange  #E96401
    (1 / 7, (244, 63, 26)),    # red     #F43F1A
    (2 / 7, (249, 196, 73)),   # yellow  #F9C449
    (3 / 7, (25, 252, 142)),   # green   #19FC8E
    (4 / 7, (2, 181, 252)),    # blue    #02B5FC
    (5 / 7, (174, 129, 255)),  # purple  #AE81FF
    (6 / 7, (241, 241, 241)),  # white   #f1f1f1
    (7 / 7, (233, 100, 1)),    # orange  (wrap)
]


def lerp_color(c1, c2, t):
    """Linearly interpolate between two RGB tuples."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def get_gradient_color(t):
    """Get color at position t (0.0 to 1.0) along the gradient."""
    t = max(0.0, min(1.0, t))
    for i in range(len(COLORS) - 1):
        t0, c0 = COLORS[i]
        t1, c1 = COLORS[i + 1]
        if t <= t1:
            local_t = (t - t0) / (t1 - t0) if t1 != t0 else 0
            return lerp_color(c0, c1, local_t)
    return COLORS[-1][1]


def main():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 255))
    pixels = img.load()

    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - CENTER
            dy = y - CENTER
            dist = math.sqrt(dx * dx + dy * dy)

            # Only draw in the ring area
            if INNER_RADIUS - 2 < dist <= RADIUS + 2:
                # Angle from center, normalized to 0.0-1.0
                angle = math.atan2(dy, dx)  # -pi to pi
                t = (angle + math.pi) / (2 * math.pi)  # 0.0 to 1.0

                r, g, b = get_gradient_color(t)

                # Anti-alias outer edge
                if dist > RADIUS:
                    alpha = max(0, int(255 * (RADIUS + 2 - dist) / 2))
                    bg = 0  # black bg
                    r = int(r * alpha / 255 + bg * (255 - alpha) / 255)
                    g = int(g * alpha / 255 + bg * (255 - alpha) / 255)
                    b = int(b * alpha / 255 + bg * (255 - alpha) / 255)
                # Anti-alias inner edge
                elif dist < INNER_RADIUS:
                    alpha = max(0, int(255 * (dist - (INNER_RADIUS - 2)) / 2))
                    r = int(r * alpha / 255)
                    g = int(g * alpha / 255)
                    b = int(b * alpha / 255)

                pixels[x, y] = (r, g, b, 255)

    # Save full size and the 256x256 VS Code icon (recommended for Retina)
    img.save("icon_large.png")
    icon = img.resize((256, 256), Image.LANCZOS)
    icon.save("icon.png")
    print("Generated icon.png (256x256) and icon_large.png (512x512)")


if __name__ == "__main__":
    main()
