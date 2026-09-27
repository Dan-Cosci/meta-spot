import axios from "axios";
import { api_url } from "../config/config";

const instance = axios.create({
  baseURL: api_url
});

export default instance
