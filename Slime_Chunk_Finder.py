import random
from collections import namedtuple
from typing import List, Tuple

# BestSlimeChunks クラス
class BestSlimeChunks:
    def __init__(self):
        self.center_chunk = (0, 0)
        self.slime_chunks = []

    def __str__(self):
        return f"Chunks found: {len(self.slime_chunks)}, Center chunk: {self.center_chunk[0]}, {self.center_chunk[1]}."

# 進捗表示関数
def print_progress(progress: float):
    bar_length = 40
    block = int(round(bar_length * progress))
    progress_str = "#" * block + "-" * (bar_length - block)
    print(f"\r[{progress_str}] {int(progress * 100)}%", end='')

# ブロックをチャンクに変換
def block_to_chunk(block: int) -> int:
    return block // 16

# チャンクの中心を計算
def chunk_center(chunk: Tuple[int, int]) -> Tuple[int, int]:
    return (chunk[0] * 16 + 8, chunk[1] * 16 + 8)

# スライムチャンクかどうかを判定
def is_slime_chunk(seed: int, x_position: int, z_position: int) -> bool:
    rnd = random.Random(seed +
                        (x_position * x_position * 0x4c1906) +
                        (x_position * 0x5ac0db) + 
                        (z_position * z_position) * 0x4307a7 +
                        (z_position * 0x5f24f) ^ 0x3ad8025f)
    return rnd.randint(0, 9) == 0

# メイン関数
def main():
    seed = -8888 # Minecraftのシード値
    center = (0, 0)
    distance = 1000 # 探索範囲の半径（ブロック単位）

    best_chunks = BestSlimeChunks()
    center = (block_to_chunk(center[0]), block_to_chunk(center[1]))
    distance = block_to_chunk(distance)

    total_chunks = (2 * distance + 1) ** 2
    chunk_count = 0

    for cX in range(center[0] - distance, center[0] + distance + 1):
        for cY in range(center[1] - distance, center[1] + distance + 1):
            slime_chunks = []

            for x in range(cX - 7, cX + 7 + 1):
                for y in range(cY - 7, cY + 7 + 1):
                    offset = (x - cX, y - cY)
                    distance_squared = offset[0] ** 2 + offset[1] ** 2
                    
                    if 1 < distance_squared < 53:
                        if is_slime_chunk(seed, x, y):
                            slime_chunks.append((x, y))

            if len(slime_chunks) > len(best_chunks.slime_chunks):
                best_chunks.center_chunk = (cX, cY)
                best_chunks.slime_chunks = slime_chunks.copy()

            # 進捗を表示
            chunk_count += 1
            progress = chunk_count / total_chunks
            print_progress(progress)

    p = chunk_center(best_chunks.center_chunk)
    str_output = f"{best_chunks} Center block: {p[0]}, {p[1]}. All chunks:"
    for c in best_chunks.slime_chunks:
        str_output += f"\n{c[0]}, {c[1]}"

    print(f"\n{str_output}")
    print("Search completed.")

if __name__ == "__main__":
    main()
