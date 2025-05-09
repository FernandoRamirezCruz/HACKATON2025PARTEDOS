// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Importa las vistas de los componentes
import HelloWorld from '@/components/HelloWorld.vue'  // Ruta a HelloWorld.vue
import JuegoUno from '@/components/JuegoUno.vue'  // Ruta a JuegoUno.vue
import JuegoDos from '@/components/JuegoDos.vue'  // Ruta a JuegoDos.vue

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HelloWorld,  // Usamos HelloWorld como la ruta principal
    },
    {
      path: '/juegouno',
      name: 'JuegoUno',
      component: JuegoUno,  // Ruta para JuegoUno
    },
    {
      path: '/juegodos',
      name: 'JuegoDos',
      component: JuegoDos,  // Ruta para JuegoDos
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',  // Redirigir cualquier otra ruta al home (HelloWorld)
    }
  ],
})

export default router
