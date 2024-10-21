

# El siguiente Colab proporciona una explicación detallada sobre el funcionamiento de cada función, método y variable dentro del código de ejemplo de MuJoCo. A lo largo del notebook, se analizan en profundidad los elementos clave de la simulación, como la inicialización del entorno, la interacción con el ratón y el teclado, y el manejo de objetos en la escena simulada. Cada parte del código se desglosa para que puedas entender su propósito y cómo se utiliza en el contexto de las simulaciones físicas en tiempo real.

# Explicación detallada:
# 1. Funciones y métodos: Se explica cómo las funciones de inicialización, como `init_mujoco()`, configuran el entorno gráfico y cargan el modelo de MuJoCo. Se detallan los métodos que controlan la simulación, como `mj.mj_step()` y `mj.mj_forward()`, que avanzan la simulación en pasos discretos.
   
# 2. Eventos de entrada: Se analizan las funciones de manejo del ratón (`mouse_move()` y `mouse_button()`), que permiten que el usuario interactúe con los objetos en la simulación, y cómo estos eventos se integran en el bucle principal del programa.

# 3. Renderizado y visualización: Se examinan los métodos que actualizan y renderizan la escena, como `mj.mjr_render()`, mostrando cómo se dibuja el entorno físico en la ventana.

# 4. Variables globales: Se explora el uso de variables globales, como las posiciones del ratón y los identificadores de objetos, para almacenar el estado de la simulación y permitir la interacción en tiempo real.

# Puedes acceder al Colab en este enlace: https://colab.research.google.com/drive/1gm8F1l158Ul3IdeNbyrad75CIxx1pyW_?usp=sharing. 


import mujoco as mj
from mujoco.glfw import glfw
import numpy as np

# Variables globales para el estado del mouse y el objeto
mouse_x = 0
mouse_y = 0
button_left = False
object_name = 'green_sphere'  # Nombre del objeto a mover
object_id = None

# Inicialización de MuJoCo
def init_mujoco():
    global model, data, scene, cam, window, context, opt, object_id

    # Inicialización de GLFW
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    # Crear ventana
    window = glfw.create_window(1200, 900, "MuJoCo Viewer", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")
    
    # Hacer que el contexto OpenGL sea actual
    glfw.make_context_current(window)
    glfw.swap_interval(1)  # Habilitar V-Sync
    
    # MuJoCo model y data
    model = mj.MjModel.from_xml_path('balloons\\balloons.xml')
    data = mj.MjData(model)
    cam = mj.MjvCamera()
    opt = mj.MjvOption()
    scene = mj.MjvScene(model, maxgeom=10000)
    context = mj.MjrContext(model, mj.mjtFontScale.mjFONTSCALE_150.value)

    mj.mjv_defaultCamera(cam)
    mj.mjv_defaultOption(opt)
    
    # Configurar callbacks de mouse
    glfw.set_cursor_pos_callback(window, mouse_move)
    glfw.set_mouse_button_callback(window, mouse_button)
    
    # Obtener el ID del objeto para actualizar su posición
    object_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, object_name)

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


def mouse_move(window, xpos, ypos):
    global mouse_x, mouse_y
    mouse_x = xpos
    mouse_y = ypos

def mouse_button(window, button, action, mods):
    global button_left
    if button == glfw.MOUSE_BUTTON_LEFT:
        button_left = (action == glfw.PRESS)

def update_object_position():
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
        
        model.geom_pos[object_id] = new_position

def main():
    init_mujoco()
    
    while not glfw.window_should_close(window):
        mj.mj_step(model, data)
        mj.mj_forward(model, data)
        
        # Actualizar la posición del objeto si el botón izquierdo está presionado
        if button_left:
            update_object_position()
        
        # Actualizar la escena y renderizar
        mj.mjv_updateScene(model, data, opt, None, cam, mj.mjtCatBit.mjCAT_ALL.value, scene)
        mj.mjr_render(mj.MjrRect(0, 0, 1200, 900), scene, context)
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
