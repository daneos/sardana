from sardana.macroserver.macro import Macro, Type
import json
import math


class DiscretePseudoMotorConfiguration(dict):
    def __init__(self, pseudo_obj, macro):
        self.pseudo = pseudo_obj
        self.macro = macro
        _physical_motor_name = self.pseudo.physical_elements[0]
        self.motor = macro.getMoveable(_physical_motor_name)
        conf = self.get_configuration()
        super(DiscretePseudoMotorConfiguration, self).__init__(conf)

    def get_configuration(self):
        return json.loads(self.pseudo.read_attribute('configuration').value)

    def has_calibration(self):
        return all(['set' in self[x].keys() for x in self.keys()])

    def add_point(self, label, pos, dmin, dmax, set):
        point = dict()
        point['pos'] = int(pos)
        # Calculate point calibration if required
        if self.has_calibration():
            # Set to current physical position if no value supplied as argument
            if math.isinf(set):
                point['set'] = self.motor.position
            else:
                point['set'] = float(set)
            # If point exists, we use current min, max values
            if label in self.keys() and math.isinf(dmin) and math.isinf(dmax):
                p = self[label]
                min_pos = point['set'] - abs(p['set'] - p['min'])
                max_pos = point['set'] + abs(p['set'] - p['max'])
            # else, new point has new calibration,
            else:
                min_pos = point['set'] - dmin
                max_pos = point['set'] + dmax

            point['min'] = min_pos
            point['max'] = max_pos

        self[label] = point
        self._update()

    def remove_point(self, label):
        try:
            self.pop(label)
            self._update()
        except Exception as e:
            self.macro.error('Cannot remove label {0}\n{1}'.format(label, e))

    def _update(self):
        try:
            self.pseudo.write_attribute('configuration', json.dumps(self))
            self.macro.debug('Updated configuration:\n{0}'.format(self))
        except Exception as e:
            msg = 'Cannot update configuration]\n{0}\{1}'.format(e, self)
            self.macro.error(msg)

    def __str__(self):
        return json.dumps(self, indent=4, sort_keys=True)


class def_dpm_pos(Macro):
    """
    Define a (calibrated) point for a discrete pseudomotor configuration.

    The mandatory parameters to execute the macro are: pseudo, label and pos.

    Two different scenarios exist: To define a new point or to modify an
    existing one. The controller protects from uploading repeated pos values.

    If the point is new, the default dmin and dmax parameters are used to
    construct the calibration. If no set point is provided, the current
    physical position is used instead.

    If the point already exists, the values are updated as in the previous
    case. However, if no dmin and dmax are provided, the previous
    calibration values for dmin and dmax are calculated and used to rebuild
    the calibration.
    """
    param_def = [
        ['pseudo', Type.PseudoMotor, None, 'Discrete pseudomotor name'],
        ['label', Type.String, None, 'Label name'],
        ['pos', Type.Integer, None, 'Pseudo position'],
        ['dmin', Type.Float, float('-inf'),
         'Delta increment defining the minimum position'],
        ['dmax', Type.Float, float('inf'),
         'Delta increment defining the maximum position'],
        ['set', Type.Float, float('inf'), 'Real position'],
        ]

    def run(self, pseudo, label, pos, dmin, dmax, set):
        conf = DiscretePseudoMotorConfiguration(pseudo, self)
        conf.add_point(label, pos, dmin, dmax, set)


class udef_dpm_pos(Macro):
    """
    Remove a point from a discrete pseudomotor configuration.
    """
    param_def = [
        ['pseudo', Type.PseudoMotor, None, 'Discrete pseudomotor name'],
        ['label', Type.String, None, 'Label name'],
    ]

    def run(self, pseudo, label):
        conf = DiscretePseudoMotorConfiguration(pseudo, self)
        conf.remove_point(label)


class prdef_dpm_conf(Macro):
    """
    Print discrete pseudomotor configuration.
    """
    param_def = [
        ['pseudo', Type.PseudoMotor, None, 'Discrete pseudomotor name'],
    ]

    def run(self, pseudo):
        conf = DiscretePseudoMotorConfiguration(pseudo, self)
        self.output(conf)
