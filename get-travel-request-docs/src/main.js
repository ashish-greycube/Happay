import './index.css'

import { createApp } from 'vue'
// import router from './router'
import App from './App.vue'
// import { createRouter, createWebHashHistory} from 'vue-router'

import {
  Button,
  Card,
  Input,
  setConfig,
  frappeRequest,
  resourcesPlugin,
} from 'frappe-ui'

let app = createApp(App)

// const router = createRouter({
//   history: createWebHashHistory(),
//   routes: [
//     // {
//     //   name:"get-travel-request-docs",
//     //   path: "/",
//     //   component: () => import("@/App.vue")
//     // },
//     // {
//     //   path: '/success-page',
//     //   redirect: { name: '/success-page' },
//     //   name: 'success',
//     // },
//     {
//       name: "success",
//       path: "/success-page"
//     }
//   ]
// })

setConfig('resourceFetcher', frappeRequest)

// app.use(router)
app.use(resourcesPlugin)

app.component('Button', Button)
app.component('Card', Card)
app.component('Input', Input)

app.mount('#app')
