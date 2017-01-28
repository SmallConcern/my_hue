from phue import Bridge, Group
import random
import threading
import time

class CandleLight(object):
    def __init__(self, bridge_ip, set_key):
        self.light_sets = {"LR":     ["Living Room Left", "Living Room Right"],
                           "Office": ["Office"],
                           "Kitchen": ["Kitchen 1", "Kitchen 2", "Kitchen 3"]
                           }
        self.bridge = Bridge('192.168.1.120')
        self.light_dict = self.bridge.get_light_objects('name')
        self.thread_stop = threading.Event()
        self.thread = threading.Thread(target=self._candle_light, args=[])
        self.thread.daemon = True
        self.set_key = set_key

    def _get_light_set(self, set_key):
        ret_set = []
        light_keys = self.light_sets[set_key]
        for light in light_keys:
            if light in self.light_dict.keys():
                ret_set.append(self.light_dict[light])
        return ret_set

    def _adjust_lights_brightness_random(self, lights):
        for light in lights:
            self._adjust_brightness_random(light)

    def _adjust_brightness_random(self, light, min_val=0, max_val=125):
        adjustment_factors = [-50, -25 , 25, 50]
        new_value = light.brightness + random.choice(adjustment_factors)
        if new_value < min_val:
            new_value = min_val
        elif new_value > max_val:
            new_value = max_val
        light.brightness = new_value

    def _set_lights_saturation(self, lights, saturation):
        for light in lights:
            light.saturation = saturation

    def _set_lights_to_brightness(self, lights, brightness):
        for light in lights:
            light.brightness = brightness

    def _set_lights_to_hue(self, lights, hue):
        for light in lights:
            light.hue = hue

    def _turn_lights_on(self, lights):
        for light in lights:
            if not light.on:
                light.on = True

    def _candle_light(self, min_hue=6000, max_hue=8000, step=0.1):
        light_set = self._get_light_set(self.set_key)
        self._turn_lights_on(light_set)
        adjustment_factors = [-300, -200, -100, 100, 200, 300]
        current_hue = (max_hue - min_hue)/2
        self._set_lights_to_brightness(light_set, 127)
        self._set_lights_saturation(light_set, 254)
        while(True):
            time.sleep(step)
            if not self.thread_stop.isSet():
                self._adjust_lights_brightness_random(light_set)
                new_hue = current_hue + random.choice(adjustment_factors)
                if new_hue < min_hue:
                    new_hue = min_hue
                elif new_hue > max_hue:
                    new_hue = max_hue
                current_hue = new_hue
                self._set_lights_to_hue(light_set, current_hue)

    def start_flicker(self):
        print("Starting Flicker...")
        if not self.thread.is_alive():
            self.thread.start()
        else:
            self.thread_stop.clear()

    def stop_flicker(self):
        print("Stopping Flicker...")
        return self.thread_stop.set()