import axios from 'axios'

export default axios.create({
  // baseURL: 'http://localhost:5000/',
  baseURL: 'http://35.228.14.207:5000/',
  responseType: 'json'
})