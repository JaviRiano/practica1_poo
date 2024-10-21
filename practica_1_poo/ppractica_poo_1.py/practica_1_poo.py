import mujoco as mj
from mujoco.glfw import glfw
import numpy as np


# Variables globales para el estado del mouse y el objeto
mouse_x = 0
mouse_y = 0
button_left = False
object_name = 'green_sphere'  # Nombre del objeto a mover
object_id = None


class simulator:    


    # Inicialización de MuJoCo
    def __init__(self,path):
        #global model, data, scene, cam, window, context, opt, object_id

        # Inicialización de GLFW
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        # Crear ventana
        self.window = glfw.create_window(1200, 900, "MuJoCo Viewer", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        
        # Hacer que el contexto OpenGL sea actual
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # Habilitar V-Sync
        
        # MuJoCo model y data
        self.model = mj.MjModel.from_xml_path(path)
        self.data = mj.MjData(self.model)
        self.cam = mj.MjvCamera()
        self.opt = mj.MjvOption()
        self.scene = mj.MjvScene(self.model, maxgeom=10000)
        self.context = mj.MjrContext(self.model, mj.mjtFontScale.mjFONTSCALE_150.value)

        mj.mjv_defaultCamera(self.cam)
        mj.mjv_defaultOption(self.opt)
        
        # Configurar callbacks de mouse
        glfw.set_cursor_pos_callback(self.window, self.mouse_move)
        glfw.set_mouse_button_callback(self.window, self.mouse_button)
        
        # Obtener el ID del objeto para actualizar su posición
        object_id = mj.mj_name2id(self.model, mj.mjtObj.mjOBJ_GEOM, object_name)

    def keyboard(self, window, key, scancode, act, mods):
        # Resetea la simulación con la tecla BACKSPACE
        if act == glfw.PRESS and key == glfw.KEY_BACKSPACE:
            mj.mj_resetData(self.model, self.data)
            mj.mj_forward(self.model, self.data)
            for i in range(len(self.initial_joint_angles)):
                self.data.qpos[i] = self.initial_joint_angles[i]
            mj.mj_forward(self.model, self.data)
        
        # Activa la interacción con la tecla A o a
        if act == glfw.PRESS and (key == glfw.KEY_A or key == glfw.KEY_A):
            self.interact_with_object()


    def mouse_move(self,window, xpos, ypos):
        global mouse_x, mouse_y
        mouse_x = xpos
        mouse_y = ypos

    def mouse_button(self,window, button, action, mods):
        global button_left
        if button == glfw.MOUSE_BUTTON_LEFT:
            button_left = (action == glfw.PRESS)

    def update_object_position(self):
        if object_id is not None:
            # Convertir las coordenadas del mouse a una posición en el mundo
            # Aquí se asume una conversión simple para demostrar el concepto.
            # En un caso real, deberías aplicar una transformación más precisa.
            scale_factor = 0.001  # Factor de escala para convertir el movimiento del mouse a unidades del mundo
            new_position = np.array([
                (mouse_x - 600) * scale_factor,  # Ajustar según el centro de la ventana
                (450 - mouse_y) * scale_factor,  # Ajustar según el centro de la ventana
                0.2  # Mantener la posición en Z constante, o ajustarla según sea necesario
            ])
            
            self.model.geom_pos[object_id] = new_position

    def run(self):
        while not glfw.window_should_close(self.window):
            mj.mj_step(self.model, self.data)
            mj.mj_forward(self.model, self.data)
            
            # Actualizar la posición del objeto si el botón izquierdo está presionado
            if button_left:
                self.update_object_position()
            
            # Actualizar la escena y renderizar
            mj.mjv_updateScene(self.model, self.data, self.opt, None, self.cam, mj.mjtCatBit.mjCAT_ALL.value, self.scene)
            mj.mjr_render(mj.MjrRect(0, 0, 1200, 900), self.scene, self.context)
            
            glfw.swap_buffers(self.window)
            glfw.poll_events()

        glfw.terminate()



def main():
    simulation=simulator("balloons\\balloons.xml")#editar 
    simulation.run()

if __name__ == "__main__":
    main()    