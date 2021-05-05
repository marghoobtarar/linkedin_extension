import { useState } from 'react';
import './App.css';
import axios from 'axios'

function App() {
  const [email, setEmail]=useState()
  const [password, setPassword] = useState()
  const submitLogin = e=>{
    e.preventDefault()
    axios.post('http://127.0.0.1:8000/scrap/automate/',{'email':email,'password':password}).then(res=>{
      console.log(res.data)
    }).catch((err)=>{
      console.log(err)
    })

  }
  return (
    <div className="App">
      <div>
        <h2>
          Please provide your linkedin credentials
        </h2>
      </div>
      <form onSubmit={e=>submitLogin(e)}>
      <div>
      <input  placeholder='enter the email'  onChange={e=>setEmail(e.target.value)}/>
      </div>
      <div>
      <input placeholder='enter the password' onChange={e=>setPassword(e.target.value)}/>

      </div>
      <input type='Submit'/>
      </form>
    </div>
  );
}

export default App;
