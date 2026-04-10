import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IMMDeviceEnumerator
from comtypes import GUID

class VolumeController:
    def __init__(self):
        try:
            # 1. Definimos el ID de la interfaz de volumen
            IID_IAudioEndpointVolume = GUID("{5CDF2C82-841E-4546-9722-0CF74078229A}")
            
            # 2. Usamos el enumerador de dispositivos directamente
            enumerator = AudioUtilities.GetDeviceEnumerator()
            
            # 3. Obtenemos el dispositivo de salida por defecto (0 = Render, 1 = Multimedia)
            devices = enumerator.GetDefaultAudioEndpoint(0, 1)
            
            # 4. Ahora sí activamos la interfaz
            self.interface = devices.Activate(
                IID_IAudioEndpointVolume, CLSCTX_ALL, None)
            
            self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
            
            # 5. Configuramos el rango
            self.volRange = self.volume.GetVolumeRange()
            self.minVol = self.volRange[0]
            self.maxVol = self.volRange[1]
            print("Control de Audio: Conectado correctamente")
            
        except Exception as e:
            print(f"Error fatal en el control de audio: {e}")
            raise e

    def set_volume(self, length):
        # Mapeo de distancia a volumen (ajusta [20, 200] si tu mano está lejos/cerca)
        vol = np.interp(length, [20, 200], [self.minVol, self.maxVol])
        volBar = np.interp(length, [20, 200], [400, 150])
        volPer = np.interp(length, [20, 200], [0, 100])
        
        self.volume.SetMasterVolumeLevel(vol, None)
        return int(volBar), int(volPer)