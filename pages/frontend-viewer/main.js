import { IFCLoader } from "./vendor/IFCLoader.js";
import {
  AmbientLight,
  AxesHelper,
  DirectionalLight,
  GridHelper,
  PerspectiveCamera,
  MeshLambertMaterial,
  Scene,
  Raycaster,
  Vector2,
  WebGLRenderer,
} from "./vendor/three.module.js";
import { OrbitControls } from "./vendor/OrbitControls.js";

import {
  acceleratedRaycast,
  computeBoundsTree,
  disposeBoundsTree
} from './vendor/three-mesh-bvh/three-mesh-bvh.js';

/*=====DESCRIPCION GENERAL DE LA FUNCIONALIDAD DEL ARCHIVO :*/

/*Este es un módulo que carga un modelo 3D desde un archivo IFC y lo renderiza usando la 
biblioteca Three.js en un navegador web. El módulo importa varias clases de la biblioteca 
Three.js, incluidas IFCLoader, AmbientLight, AxesHelper, DirectionalLight, GridHelper, 
PerspectiveCamera, MeshLambertMaterial, Scene, Raycaster, Vector2 y WebGLRenderer. 
También importa OrbitControls para habilitar el control del mouse del modelo renderizado, 
y Raycast acelerado, computeBoundsTree y disposeBoundsTree de la biblioteca three-mesh-bvh, 
que se utilizan para optimizar el rendimiento del proceso de renderizado.
El módulo define una función setup() que configura la escena, la cámara, las luces, los 
controles del mouse y el renderizador de Three.js. También configura la carga de IFC y 
agrega un detector de eventos para cambiar el tamaño de la ventana gráfica. Además, hay dos 
materiales, preselectMat y selectMat, que definen la apariencia del modelo cuando se 
preselecciona o selecciona, respectivamente. El módulo define dos funciones, getIntersection(evento) 
y getObjectData(evento), que se utilizan para seleccionar objetos en el modelo. La función 
getIntersection(evento) proyecta un rayo desde la posición del mouse y devuelve el objeto que se 
cruza, mientras que la función getObjectData(evento) devuelve las propiedades y los conjuntos de 
propiedades del objeto seleccionado.*/


// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.


/*=====DESCRIPCION DETALLADA POR FUNCIONES O SCRIPTS:*/

/*Este código está creando un array vacío llamado "ifcModels" y una instancia 
de la clase "IFCLoader" llamada "ifcLoader". La clase IFCLoader es una utilidad de 
Three.js, una biblioteca de gráficos 3D en JavaScript, que se utiliza para cargar 
modelos en formato IFC (Industry Foundation Classes), que es un formato de archivo 
utilizado para la interoperabilidad de software en la industria de la construcción.
Además, el código está definiendo un objeto "size" que tiene dos propiedades: 
"width" y "height". Estas propiedades están siendo asignadas a los valores de 
la anchura y altura de la ventana del navegador utilizando los objetos del 
navegador "window.innerWidth" y "window.innerHeight", respectivamente.*/
const ifcModels = [];
const ifcLoader = new IFCLoader();
const size = {
  width: window.innerWidth,
  height: window.innerHeight,
};


/*Este código crea un nuevo material MeshLambertMaterial y lo asigna a 
  la constante preselectMat. Este material es utilizado para representar 
  la apariencia visual de un objeto en una escena 3D renderizada con Three.js.
  Las propiedades que se establecen en el material son las siguientes:
  transparent: true: esto indica que el material es transparente.
  opacity: 0.6: esto establece el nivel de opacidad del material en un 60%.
  color: 0xf1a832: esto establece el color del material en un tono dorado.
  depthTest: false: esto desactiva la prueba de profundidad en el material, 
  lo que significa que siempre se renderizará encima de otros objetos, incluso 
  si están más cerca de la cámara.*/
const preselectMat = new MeshLambertMaterial({
  transparent: true,
  opacity: 0.6,
  color: 0xf1a832,
  depthTest: false
})

/*===============cambio de color========================================*/


/*Este código define un material para una malla (Mesh) que se utilizará para 
resaltar elementos seleccionados en una escena de tres.js. El material se crea 
utilizando la clase MeshLambertMaterial y se especifican las siguientes propiedades:

transparent: true: indica que el material es transparente.
opacity: 0.6: establece la opacidad del material en un 60%.
color: 0x6aa84f: establece el color del material en un tono de verde claro.
depthTest: false: indica que la prueba de profundidad se desactiva para el 
material, lo que significa que no se verá afectado por otros objetos que se 
encuentren detrás de él en la escena.*/
const selectMat = new MeshLambertMaterial({
  transparent: true,
  opacity: 0.6,
  color: 0x6aa84f,
  depthTest: false
})


/*Esta función es parte de una aplicación web desarrollada con Streamlit, 
  una plataforma para la creación de aplicaciones web interactivas en Python. 
  La función sendValue() se utiliza para enviar un valor de retorno desde el 
  componente personalizado que se ha creado en la aplicación y establecer este 
  valor como el valor actual del componente. En otras palabras, esta función 
  permite que el componente personalizado interactúe con la aplicación y 
  proporcione valores que pueden ser utilizados por otras partes de la aplicación.*/
function sendValue(value) {
  Streamlit.setComponentValue(value)
}

/*La función setup() establece una escena básica en Three.js, que incluye una cámara, 
  luces, controles de mouse, renderizador y objetos adicionales como rejillas, ejes 
  y selecciones de objetos. La función también configura la carga de modelos IFC y 
  la detección de intersección con el mouse para resaltar y seleccionar objetos en la 
  escena. Cuando un objeto es seleccionado, se llama a la función sendValue() para 
  enviar los datos del objeto seleccionado al backend de Python a través de Streamlit. 
  En general, la función setup() configura y establece una escena interactiva en Three.js 
  que puede ser utilizada para visualizar y manipular modelos 3D.*/

function setup(){
  //BASIC THREE JS SCENE, CAMERA, LIGHTS, MOUSE CONTROLS
    window.scene = new Scene();
    const ifc = ifcLoader.ifcManager;

    //Creates the camera (point of view of the user)
    const camera = new PerspectiveCamera(75, size.width / size.height);
    camera.position.z = 15;
    camera.position.y = 13;
    camera.position.x = 8;
  
    //Creates the lights of the scene
    const lightColor = 0xffffff;
    const ambientLight = new AmbientLight(lightColor, 0.5);
    window.scene.add(ambientLight);
    const directionalLight = new DirectionalLight(lightColor, 1);
    directionalLight.position.set(0, 10, 0);
    directionalLight.target.position.set(-5, 0, 0);
    window.scene.add(directionalLight);
    window.scene.add(directionalLight.target);
    window.scene.add(directionalLight.target);
  
    //Sets up the renderer, fetching the canvas of the HTML
    const threeCanvas = document.getElementById("three-canvas");
    const renderer = new WebGLRenderer({ canvas: threeCanvas, alpha: true });
    renderer.setSize(size.width, size.height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  
    //Creates grids and axes in the window.scene
    const grid = new GridHelper(50, 30);
    window.scene.add(grid);
    const axes = new AxesHelper();
    axes.material.depthTest = false;
    axes.renderOrder = 1;
    window.scene.add(axes);
  
    //Creates the orbit controls (to navigate the scene)
    const controls = new OrbitControls(camera, threeCanvas);
    controls.enableDamping = true;
    controls.target.set(-2, 0, 0);
  
    //Animation loop
    const animate = () => {
      controls.update();
      renderer.render(window.scene, camera);
      requestAnimationFrame(animate);
    };
  
    animate();
  
    //Adjust the viewport to the size of the browser
    window.addEventListener("resize", () => {
      (size.width = window.innerWidth), (size.height = window.innerHeight);
      camera.aspect = size.width / size.height;
      camera.updateProjectionMatrix();
      renderer.setSize(size.width, size.height);
    });
  
    //Sets up the IFC loading

    ifc.setWasmPath("./vendor/IFC/");

    ifc.setupThreeMeshBVH(
      computeBoundsTree,
      disposeBoundsTree,
      acceleratedRaycast
      );
  
    // SELECTOR EXAMPLE
    const raycaster = new Raycaster();
      raycaster.firstHitOnly = true;
      const mouse = new Vector2();
    
      /*La función getIntersection se encarga de obtener el objeto 3D 
        que es intersectado por un rayo que se emite desde la posición del 
        mouse en la pantalla. Para hacer esto, la función primero calcula 
        la posición del mouse en la pantalla en relación a los límites de 
        un canvas, que es donde se dibujan los modelos 3D. Luego, se coloca 
        un raycaster en la cámara y se apunta hacia la posición del mouse. El 
        raycaster se utiliza para determinar qué objetos 3D en la escena están 
        siendo intersectados por el rayo. Si se encuentra un objeto, la función 
        devuelve un objeto con el ID del objeto IFC (Industry Foundation Classes) 
        que se ha encontrado y el ID del modelo al que pertenece. Este objeto 
        se utiliza en la función getObjectData para recuperar las propiedades 
        y conjuntos de propiedades asociadas con el objeto IFC.*/
        function getIntersection(event) {
    
        // Computes the position of the mouse on the screen
        const bounds = threeCanvas.getBoundingClientRect();
        const x1 = event.clientX - bounds.left;
        const x2 = bounds.right - bounds.left;
        mouse.x = (x1 / x2) * 2 - 1;

        const y1 = event.clientY - bounds.top;
        const y2 = bounds.bottom - bounds.top;
        mouse.y = -(y1 / y2) * 2 + 1;
    
        // Places the raycaster on the camera, pointing to the mouse
        raycaster.setFromCamera(mouse, camera);
    
        // Casts a ray
        const found = raycaster.intersectObjects(ifcModels)

        // Gets Express ID
        if (found[0]) { 
          const index = found[0].faceIndex;
          const geometry = found[0].object.geometry;
          return {"id":ifc.getExpressId(geometry, index), "modelID": found[0].object.modelID}
        }
        ;
    }

      /*La función getObjectData(event) toma un objeto de evento como argumento y 
      devuelve una cadena de texto JSON que contiene información sobre un objeto 
      3D que se intersecta con un rayo que se lanza desde el evento. Esta información 
      incluye el identificador del objeto, sus propiedades y conjuntos de propiedades.
      Primero, la función llama a getIntersection(event) para obtener el objeto 
      intersectado y lo asigna a la variable intersection. Si intersection existe, 
      la función llama a ifc.getItemProperties(intersection.modelID, objectId) y 
      ifc.getPropertySets(intersection.modelID, objectId, true) para obtener las 
      propiedades y conjuntos de propiedades del objeto, respectivamente. Luego, la 
      función construye un objeto de datos con el identificador del objeto y sus 
      propiedades y conjuntos de propiedades, y devuelve una cadena de texto JSON que 
      representa este objeto de datos utilizando JSON.stringify().*/
      function getObjectData(event) {
        const intersection = getIntersection(event);
        if (intersection){
          const objectId = intersection.id;
          const props = ifc.getItemProperties(intersection.modelID, objectId);
          const propsets = ifc.getPropertySets(intersection.modelID, objectId,true);
          let data = {
            "id": objectId,
            "props": propsets,
          }
          return JSON.stringify(data, null, 2)
        }
      }
      
    // HIGHLIGHT
    // References to the previous selections
      const highlightModel = { id: - 1};
      const selectModel = { id: - 1};
    function highlight(event, material, model) {
    const intersection = getIntersection(event)
    if (intersection) {
        // Creates subset
        ifc.createSubset({
            modelID: intersection.modelID,
            ids: [intersection.id],
            material: material,
            scene: window.scene,
            removePrevious: true
        })
    } 
    else {
        // Remove previous highlight
        ifc.removeSubset(model.id, window.scene, material);
    }
    }
    
    // Pre-Highlight Materials
    window.onmousemove = (event) => highlight(event, preselectMat, highlightModel);
      
    // Highlight Selected Object and send Object data to Python
      window.ondblclick = (event) => {
        highlight(event, selectMat, selectModel);
        let data = getObjectData(event);
        sendValue(data)
      }
}

async function sigmaLoader (url, ifcLoader){
  const ifcModel = await ifcLoader.ifcManager.parse(url.buffer)
  ifcModels.push(ifcModel.mesh)
  window.scene.add(ifcModel.mesh)
}
    
/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */

 async function loadURL(event) {
  if (!window.rendered) {
    const {url} = event.detail.args;
    await sigmaLoader(url, ifcLoader);
    window.rendered = true
  }
}

Streamlit.loadViewer(setup)
// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, loadURL)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(window.innerWidth/2)