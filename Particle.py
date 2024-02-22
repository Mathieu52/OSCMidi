class Particle:
    def __init__(self, note: int, lifetime: float):
        self.note = note
        self.lifetime = lifetime

    def __str__(self):
        return f"Particle(note={self.note}, lifetime={self.lifetime})"
