from manim import *
from functions import *


class MonopolyAnimation(ThreeDScene):

    def construct(self):
        """
        :return: Build the Monopoly animation scene.
        """
        path1 = VGroup(
            *[VGroup(Rectangle(WHITE, 6, 3), Rectangle(WHITE, 1.4, 3)) for _ in range(9)]
        ).arrange(buff=0).rotate(90 * DEGREES)

        for location in path1:
            location[1].align_to(location[0], RIGHT)

        path2 = path1.copy().rotate(270 * DEGREES)
        path3 = path2.copy().rotate(270 * DEGREES)
        path4 = path3.copy().rotate(270 * DEGREES)

        start_location = VGroup(Square(6), Tex("Start").rotate(90 * DEGREES).scale(4)).shift(np.array([6, 6, -6]))
        visit_jail_location = VGroup(Square(6), Tex("Jail").rotate(90 * DEGREES).scale(4))
        parking_location = VGroup(Square(6), Tex("Parking").scale(0.7).rotate(90 * DEGREES).scale(4))
        go_to_jail_location = VGroup(Square(6), VGroup(Tex("Go to"), Tex("Jail")).arrange_in_grid(2, 1).rotate(90 * DEGREES).scale(4))

        path1.next_to(start_location, DOWN, buff=0)
        visit_jail_location.next_to(path1, DOWN, buff=0)
        path2.next_to(visit_jail_location, LEFT, buff=0)
        parking_location.next_to(path2, LEFT, buff=0)
        path3.next_to(parking_location, UP, buff=0)
        go_to_jail_location.next_to(path3, UP, buff=0)
        path4.next_to(go_to_jail_location, RIGHT, buff=0)

        locations = VGroup(start_location, *path1[::-1], visit_jail_location, *path2[::-1],
                           parking_location, *path3[::-1], go_to_jail_location, *path4[::-1])

        self.add(locations)  # adding to manim scene

        for i in [1, 3]:
            locations[i][1].set_fill(PINK, 0.8)
        for i in [6, 8, 9]:
            locations[i][1].set_fill(PURE_BLUE, 0.8)
        for i in [11, 13, 14]:
            locations[i][1].set_fill(LIGHT_PINK, 0.8)
        for i in [16, 18, 19]:
            locations[i][1].set_fill(YELLOW, 0.8)
        for i in [21, 23, 24]:
            locations[i][1].set_fill(ORANGE, 0.8)
        for i in [26, 27, 29]:
            locations[i][1].set_fill(PURE_RED, 0.8)
        for i in [31, 32, 34]:
            locations[i][1].set_fill(GREEN, 0.8)
        for i in [36, 39]:
            locations[i][1].set_fill(BLUE, 0.8)  # Bitola and Skopje <3

        for i in [2, 4, 5, 7, 12, 15, 17, 22, 25, 28, 33, 35, 37, 38]:
            locations[i][1].set_opacity(0)

        for i in [5, 15, 25, 35]:
            locations[i][0].set_fill(YELLOW_A, 0.7)

        self.set_camera_orientation(0 * DEGREES, 0 * DEGREES, zoom=0)
        self.wait(0.2)
        self.move_camera(0 * DEGREES, 0 * DEGREES, zoom=0.25, frame_center=[-10, -10, 0])
        self.wait(1)
        self.move_camera(45 * DEGREES, 30 * DEGREES, zoom=0.3, frame_center=[5, -3, -4])
        self.wait(1)

        turn = 0
        iteration_label = MathTex(f"n=", turn).next_to(locations[0][0], UP, 2.5).scale(2.5).rotate(90 * DEGREES)
        self.play(Write(iteration_label))  # play manim scene animation

        prisms = VGroup(
            *[Prism((2, 2, 0)).next_to(locations[i][0], OUT, buff=0).set_fill(RED, 0).set_z_index(10) for i in range(40)]
        )

        current_distribution = generate_init_vector()
        transition_matrix = t_matrix()

        for _ in range(15):  # showcase 15 iterations of player movement
            current_prisms = VGroup()
            animations = []
            for i, proba in enumerate(current_distribution):
                if proba == 0:
                    current_prisms.add(Prism((2, 2, 0)).next_to(locations[i][0], OUT, buff=0).set_fill(RED, 0).set_z_index(1000+i))
                    animations.append(Transform(prisms[i], current_prisms[i]))
                else:
                    current_prisms.add(Prism((2, 2, 40 * proba if 40 * proba < 15 else 15)).next_to(locations[i][0], OUT, buff=0).set_fill(RED, 1).set_z_index(1000+i))
                    animations.append(Transform(prisms[i], current_prisms[i]))

            self.play(AnimationGroup(
                *animations,
                Transform(iteration_label,  MathTex(f"n=", turn).next_to(locations[0][0], UP, 2.5).scale(2.5).rotate(90 * DEGREES)))
            )

            if turn == 0:
                self.wait(2)

            turn += 1
            current_distribution = np.matmul(current_distribution, transition_matrix).tolist()

        stationary_distribution = generate_stationary_vector()
        current_prisms = VGroup()
        animations = []

        for i, proba in enumerate(stationary_distribution):
            if proba == 0:
                current_prisms.add(Prism((2, 2, 0)).next_to(locations[i][0], OUT, buff=0).set_fill(GOLD, 0).set_z_index(1000+i))
                animations.append(Transform(prisms[i], current_prisms[i]))
            else:
                current_prisms.add(Prism((2, 2, 40 * proba if 40 * proba < 15 else 15)).next_to(locations[i][0], OUT, buff=0).set_fill(GOLD, 1).set_z_index(1000+i))
                animations.append(Transform(prisms[i], current_prisms[i]))

        self.play(AnimationGroup(*animations, Transform(iteration_label,  MathTex(f"n=", f"\infty").next_to(locations[0][0], UP, 2.5).scale(2.5).rotate(90 * DEGREES))))

        self.wait(2)
        self.move_camera(45 * DEGREES, -100 * DEGREES, zoom=0.3, frame_center=[-13, -24, -4])
        self.wait(1)
        self.move_camera(0 * DEGREES, 0 * DEGREES, zoom=0.25, frame_center=[-10, -10, 0])
        self.wait(1)
        self.move_camera(0, 0, zoom=0)

        self.wait(1)
