import argparse

import numpy as np
import torch
from diffco.model import RevolutePlanarRobot

from generate_batch_data_2d import generate_data_planar_manipulators


predefined_obstacles = {
    # ('circle', (3, 2), 2), #2circle
    # ('circle', (-2, 3), 0.5), #2circle
    # ('rect', (-2, 3), (1, 1)),
    # ('rect', (1.7, 3), (2, 3)),
    # ('rect', (-1.7, 3), (2, 3)),
    # ('rect', (0, -1), (10, 1)),
    # ('rect', (8, 7), 1),
    '1rect_1circle': [('rect', (4, 3), (2, 2)),
        ('circle', (-4, -3), 1)],
    # ('rect', (4, 3), (2, 2)), # 2rect
    # ('rect', (-4, -3), (2, 2)) # 2rect
    # ('rect', (3, 2), (2, 2)) # 1rect
    '3circle': [
        ('circle', (0, 4.5), 1), #3circle
        ('circle', (-2, -3), 2), #3circle
        ('circle', (-2, 2), 1.5), #3circle
    ],
    '1rect_1circle_7d': [
        ('circle', (-2, 3), 1), #1rect_1circle_7d
        ('rect', (3, 2), (2, 2)) #1rect_1circle_7d
    ],
    '2class_1': [
        ('rect', (5, 0), (2, 2), 0), #2class_1
        ('circle', (-3, 6), 1, 1), #2class_1
        ('rect', (-5, 2), (2, 1.5), 1), #2class_1
        ('circle', (-5, -2), 1.5, 1), #2class_1
        ('circle', (-3, -6), 1, 1) #2class_1
    ],
    '2class_2': [
        ('rect', (0, 3), (16, 0.5), 1), #2class_2
        ('rect', (0, -3), (16, 0.5), 0), #2class_2
    ],
    # ('rect', (-7, 3), (2, 2)) #1rect_active
    '3circle_7d': [
        ('circle', (-2, 2), 1), #3circle_7d
        ('circle', (-3, 3), 1), #3circle
        ('circle', (-6, -3), 1) #3circle
    ]
    # ('rect', (5, 4), (4, 4), 0), #2instance_big
    # ('circle', (-5, -4), 2, 1) #2instance_big
}


def main(
        env_name: str = '3d_halfnarrow',
        folder: str = 'data/landscape',
        label_type: str = 'binary',
        num_class: int = 2,
        dof: int = 3,
        num_init_points: int = 8000,
        random_seed: int = 2021,
        width: float = 0.3) -> None:
    torch.manual_seed(random_seed)
    np.random.seed(random_seed)

    if env_name == '7d_narrow':
        obstacles = []
        lb = np.array([-8, 1.0], dtype=float)
        ub = np.array([8, 8], dtype=float)
        for i in range(150):
            pos = np.random.rand(2,)*(ub-lb)+lb
            pos = pos.tolist()
            size = (1, 1)
            obstacles.append(('rect', pos, size))
        
        lb = np.array([-8, -8], dtype=float)
        ub = np.array([8, -1.0], dtype=float)
        for i in range(150):
            pos = np.random.rand(2,)*(ub-lb)+lb
            pos = pos.tolist()
            size = (1, 1)
            obstacles.append(('rect', pos, size))
        link_length = 1
    elif env_name == '3d_halfnarrow':
        obstacles = []
        lb = np.array([-8, 1.0], dtype=float)
        ub = np.array([8, 8], dtype=float)
        for i in range(150):
            pos = np.random.rand(2,)*(ub-lb)+lb
            pos = pos.tolist()
            size = (1, 1)
            obstacles.append(('rect', pos, size))

        link_length = 2.5
    else:
        obstacles = predefined_obstacles[env_name]
        lengths = {2: 3.5, 3: 2, 7:1}
        link_length = lengths[dof]
    
    robot = RevolutePlanarRobot(link_length, width, dof) # (7, 1), (2, 3)

    generate_data_planar_manipulators(robot, folder, obstacles, label_type=label_type,
        num_class=num_class, num_points=num_init_points, env_id=env_name, vis=True)
    return

if __name__ == "__main__":
    desc = '2D data generation'
    parser = argparse.ArgumentParser(description=desc)
    env_choices = ['1rect_1circle', '3circle', '1rect_1circle_7d', '2class_1',
                   '2class_2', '3circle_7d', '7d_narrow', '3d_halfnarrow']
    parser.add_argument('-e', '--env', dest='env_name', help='2D environment', choices=env_choices, default='3d_halfnarrow')
    parser.add_argument('-o', '--output-dir', dest='folder', default='data/landscape')
    parser.add_argument('-l', '--label-type', choices=['instance', 'class', 'binary'], default='binary')
    parser.add_argument('-n', '--num-classes', dest='num_class', default=2, type=int)
    parser.add_argument('-d', '--dof', help='degrees of freedom', choices=[2, 3, 7], default=3, type=int)
    parser.add_argument('-i', '--num-init-points', type=int, default=8000)
    parser.add_argument('-w', '--width', help='link width', type=float, default=0.3)
    parser.add_argument('-r', '--random-seed', type=int, default=2021)
    args = parser.parse_args()
    main(**vars(args))
