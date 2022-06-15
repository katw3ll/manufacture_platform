import { getResponse } from "../utils/utils";

const API_URL = "http://194.87.99.23:8000";
// const API_URL = "http://localhost:8000/api";

class Api {
    constructor() {
      this._api = "http://localhost:8000/api";
    }

    // AUTHORIZATION

    auth(data) {
      return fetch(`${API_URL}/api/token/login/`, {
        method: "POST",
        headers: {
          // "Access-Control-Allow-Origin": '*'
          // "Content-Type": "multipart/form-data",
        },
        body: new FormData( document.getElementById('login__form') )
      }).then(getResponse);
    }

    getCurrentUser() {
      return fetch(`${API_URL}/auth/user/me`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        }

      }).then(getResponse)
    }

    getOrderList() {
      return fetch(`${API_URL}/api/get_project`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Token ${localStorage.getItem('jwt')}`,
          },

        }).then(getResponse);
    }

    deleteProject(data) {
      return fetch(`${API_URL}/api/delete_project`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }

    getComplect() {
      return fetch(`${API_URL}/api/composition/?limit=100&offset=0`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },

      }).then(getResponse);
    }

    getMaterialBySelectOrders(data) {
      return fetch(`${API_URL}/api/project_cutting2`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }

    getMap(data) {
      return fetch(`${API_URL}/api/cutting`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)

      }).then(getResponse);
    }

    saveCuts(data) {
      return fetch(`${API_URL}/api/save_cutting`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)

      }).then(getResponse);
    }

    getStoreItems(type) {
      return fetch(`${API_URL}/api/show_materials_in_stock`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify({material_type: type})

      }).then(getResponse);
    }

    searchLengths(data) {
      return fetch(`${API_URL}/api/lengths_search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)

      }).then(getResponse);
    }

    searchAccessories(data) {
      return fetch(`${API_URL}/api/accessories_search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)

      }).then(getResponse);
    }

    addMaterialToStock(data) {
      return fetch(`${API_URL}/api/add_material_stock`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }
    addFile(file, type) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('name', file.name);
      formData.append('name_dow', type);
      return fetch(`${API_URL}/api/upload_file`, {
        method: "POST",
        headers: {
          // "Content-Type": "multipart/form-data",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: formData
      }).then(getResponse);
    }

    addQueue(data) {
      return fetch(`${API_URL}/api/add_queue`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }

    cutMaterial(data) {
      return fetch(`${API_URL}/api/save_cutting`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }

    defectCut(data) {
      return fetch(`${API_URL}/api/defect_cutting`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }

    getProjectRollets(data) {
      return fetch(`${API_URL}/api/project_rollets`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }

    getRolletComposition(data) {
      return fetch(`${API_URL}/api/project_composition`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }

    assembleTheRollet(data) {
      return fetch(`${API_URL}/api/assemble_the_roller`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }

    getAllQueue() {
      return fetch(`${API_URL}/api/queue`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
      }).then(getResponse);
    }
    getQueue(data) {
      return fetch(`${API_URL}/api/get_queue`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }

    deleteQueue(data) {
      return fetch(`${API_URL}/api/del_queue`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Token ${localStorage.getItem('jwt')}`,
        },
        body: JSON.stringify(data)
      }).then(getResponse);
    }
}

  const api = new Api();
  export default api;
