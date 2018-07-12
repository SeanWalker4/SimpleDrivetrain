import unittest
import numpy as np
from simple_drivetrain import SimpleDrivetrain


class TestCaseSimpleDrivetrain(unittest.TestCase):
    def __assertWithinRange(self, expected, observed, percent_range):
        if expected < 0:
            within_range = (observed >= (1.0 + percent_range) * expected) \
                           and (observed <= (1.0 - percent_range) * expected)
            self.assertTrue(within_range)
        elif expected > 0:
            within_range = (observed >= (1.0 - percent_range) * expected) \
                           and (observed <= (1.0 + percent_range) * expected)
            self.assertTrue(within_range)
        else:  # expected == 0
            within_range = (observed >= -percent_range) and (observed <= percent_range)
            self.assertTrue(within_range)

    def test_get_motor_vels_local_translation(self):

        norm_const = np.sqrt(2.0) / 2.0

        const_rot = (0.0, 0.0, 0.0)

        test_inputs = [[norm_const, norm_const, 0.0],
                       [0.0, 1.0, 0.0],
                       [0.0, 0.0, 1.0]]
        test_outputs = [[0.0, 1.0, 0.0, -1.0, 0.0, 0.0],
                        [norm_const, norm_const, -norm_const, -norm_const, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]

        pwm_std = (1100, 1500, 1900)

        fr = [[norm_const, norm_const, 0.0], [-norm_const, norm_const, 0.0], pwm_std]
        fl = [[-norm_const, norm_const, 0.0], [norm_const, norm_const, 0.0], pwm_std]
        bl = [[-norm_const, -norm_const, 0.0], [norm_const, -norm_const, 0.0], pwm_std]
        br = [[norm_const, -norm_const, 0.0], [-norm_const, -norm_const, 0.0], pwm_std]
        fu = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]
        bu = [[0.0, -1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]

        orientation = (0.0, 0.0, 0.0)

        testbot = SimpleDrivetrain(orientation)
        testbot.add_new_motor('fr', fr[0], fr[1], False, fr[2])
        testbot.add_new_motor('fl', fl[0], fl[1], False, fl[2])
        testbot.add_new_motor('bl', bl[0], bl[1], False, bl[2])
        testbot.add_new_motor('br', br[0], br[1], False, br[2])
        testbot.add_new_motor('fu', fu[0], fu[1], False, fu[2])
        testbot.add_new_motor('bu', bu[0], bu[1], False, bu[2])

        for i in range(0, len(test_inputs)):
            observed = testbot.get_motor_vels_local(test_inputs[i], const_rot)
            expected = test_outputs[i]

            for j in range(0, len(expected)):
                self.assertAlmostEqual(observed[j], expected[j])

    def test_get_motor_vels_local_rotation(self):
        norm_const = np.sqrt(2.0) / 2.0

        zero_vector = [0.0, 0.0, 0.0]
        rot_yaw_ccw = [0.0, 0.0, 1.0]
        rot_yaw_cw = [0.0, 0.0, -1.0]
        rot_pitch_ccw = [1.0, 0.0, 0.0]
        rot_pitch_cw = [-1.0, 0.0, 0.0]

        test_inputs = ([zero_vector, rot_yaw_ccw],
                       [zero_vector, rot_yaw_cw])
        test_outputs = ([1.0, -1.0, 1.0, -1.0, 0.0, 0.0],
                        [-1.0, 1.0, -1.0, 1.0, 0.0, 0.0])

        pwm_std = (1100, 1500, 1900)

        fr = [[norm_const, norm_const, 0.0], [-norm_const, norm_const, 0.0], pwm_std]
        fl = [[-norm_const, norm_const, 0.0], [norm_const, norm_const, 0.0], pwm_std]
        bl = [[-norm_const, -norm_const, 0.0], [norm_const, -norm_const, 0.0], pwm_std]
        br = [[norm_const, -norm_const, 0.0], [-norm_const, -norm_const, 0.0], pwm_std]
        fu = [[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]
        bu = [[0.0, -1.0, 0.0], [0.0, 0.0, 1.0], pwm_std]

        orientation = (0.0, 0.0, 0.0)

        testbot = SimpleDrivetrain(orientation)
        testbot.add_new_motor('fr', fr[0], fr[1], False, fr[2])
        testbot.add_new_motor('fl', fl[0], fl[1], False, fl[2])
        testbot.add_new_motor('bl', bl[0], bl[1], False, bl[2])
        testbot.add_new_motor('br', br[0], br[1], False, br[2])
        testbot.add_new_motor('fu', fu[0], fu[1], False, fu[2])
        testbot.add_new_motor('bu', bu[0], bu[1], False, bu[2])

        for i in range(0, len(test_inputs)):
            observed = testbot.get_motor_vels_local(test_inputs[i][0], test_inputs[i][1])
            expected = test_outputs[i]

            for j in range(0, len(expected)):
                self.__assertWithinRange(observed[j], expected[j], 0.02)