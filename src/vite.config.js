import { defineConfig } from 'vite'
//import vue from '@vitejs/plugin-vue'
import pythonVue from 'vite-plugin-vue-python'
import path from "path"

// https://vitejs.dev/config/
export default defineConfig({
  resolve:{
    alias:{
      '@/' : path.resolve(__dirname, './src')+"/"
    },
  },


  css: {
        preprocessorOptions: {
          scss: {
            additionalData: `

            `
          }
        }
      },

  plugins: [
    pythonVue("/home/zerpa/anaconda3/envs/zerpatechnology/bin/python"),
    
  ]
})
