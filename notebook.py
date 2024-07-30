import pyautogui
import random
import numpy.typing as npt
import numpy as np
import time
import math
# import Tuple
from scipy import interpolate
import list_01 as list

def mouse_bezier_curve(repeats: int = 1, move: bool = True) -> None:
    """Mouse bezier curve.

    Installing tkinter:
        https://askubuntu.com/questions/1224230/how-to-install-tkinter-for-python-3-8

    Args:
        repeats: Number of times to repeat the curve.
        move: Move the mouse or click.

    Based on:
        https://stackoverflow.com/questions/44467329/pyautogui-mouse-movement-with-bezier-curve

    """
    for _ in range(repeats):

        def point_dist(point_x1: int, point_y1: int, point_x2: int, point_y2: int) -> float:
            return math.sqrt((point_x2 - point_x1) ** 2 + (point_y2 - point_y1) ** 2)

        control_points: int = random.randint(10, 15)  # Number of control points. Must be at least 2.
        x_window_size: int
        y_window_size: int
        x_window_size, y_window_size = pyautogui.size()
        point_x1: int
        point_y1: int
        point_x2: int
        point_y2: int
        point_x1, point_y1, point_x2, point_y2 = (
            random.randint(100, x_window_size - 100),
            random.randint(200, y_window_size - 100),
            random.randint(100, x_window_size - 100),
            random.randint(200, y_window_size - 100),
        )

        # Distribute control points between start and destination evenly.
        point_x: npt.NDArray[np.int64] = np.linspace(point_x1, point_x2, num=control_points, dtype="int")
        point_y: npt.NDArray[np.int64] = np.linspace(point_y1, point_y2, num=control_points, dtype="int")

        # Randomise inner points a bit (+-random_inner_points at most).
        random_inner_points: int = 1
        random_x: list[int] = [random.randint(-random_inner_points, random_inner_points) for k in range(control_points)]
        random_y: list[int] = [random.randint(-random_inner_points, random_inner_points) for k in range(control_points)]
        random_x[0] = random_y[0] = random_x[-1] = random_y[-1] = 0
        point_x += random_x
        point_y += random_y

        # Approximate using Bezier spline.
        degree: int = 3 if control_points > 3 else control_points - 1  # Degree of b-spline. 3 is recommended.
        # Must be less than number of control points.
        ticks: npt.NDArray[np.float64]
        certain_points: npt.NDArray[np.float64]
        ticks, certain_points = interpolate.splprep([point_x, point_y], k=degree)  # noqa
        # Move upto a certain number of points
        certain_points = np.linspace(0, 1, num=2 + int(point_dist(point_x1, point_y1, point_x2, point_y2) / 25.0))
        points: npt.NDArray[np.float64]
        points = interpolate.splev(certain_points, ticks)

        # Move mouse.
        duration: float = random.uniform(0.1, 0.3)
        timeout: float = duration / len(points[0])
        point_list: list[Tuple[int, int]] = list(zip(*(i.astype(int) for i in points)))

        if move:
            for point in point_list:
                pyautogui.moveTo(*point)
                pyautogui.click()
                time.sleep(timeout)

image_path = './image.png'
def findSelectAndClick(image_path):
    time.sleep(2)  # Add a delay to ensure the screen is fully loaded
    pyautogui.screenshot('foo.png')
    # mouse_bezier_curve()
    position = pyautogui.locateCenterOnScreen(image_path)
    if position:
        pyautogui.click(position)
    else:
        # raise pyautogui.ImageNotFoundException("Image not found on screen")
        print("error")


# 定位选择框
def main():
    # try:
    #     findSelectAndClick(image_path)
    # except pyautogui.ImageNotFoundException as e:
    #     print(f"Error: {e}, not found the ui")
    findSelectAndClick(image_path) 

main()
    

