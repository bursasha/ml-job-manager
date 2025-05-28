import { BrowserRouter, Routes, Route } from 'react-router-dom';

import './App.css'
import Navbar from "./components/Navbar.tsx";
import Home from "./pages/home/Home.tsx";
import JobList from "./pages/job/jobList/JobList.tsx";
import ActiveLearningCreation from "./pages/job/jobCreation/ActiveLearningCreation.tsx";
import PreprocessingCreation from "./pages/job/jobCreation/PreprocessingCreation.tsx";
import ActiveLearningDetails from "./pages/job/jobDetails/ActiveLearningDetails.tsx";
import PreprocessingDetails from "./pages/job/jobDetails/PreprocessingDetails.tsx";
import DisplayFileSystem from "./pages/fileSystem/DisplayFileSystem.tsx";
import NotFoundPage from "./pages/NotFoundPage.tsx";


function App() {

  return (
      <BrowserRouter>
          <Navbar />
          <div className="m-4 p-2 bg-gray-200 rounded-lg">
              <Routes>
                  <Route path="/" element={<Home/>} />
                  <Route path="/jobs" element={<JobList/>} />
                  <Route path="/jobs/create/active_learning" element={<ActiveLearningCreation/>} />
                  <Route path="/jobs/create/preprocessing" element={<PreprocessingCreation/>} />
                  <Route path="/jobs/details/active_learning/:jobId" element={<ActiveLearningDetails/>} />
                  <Route path="/jobs/details/preprocessing/:jobId" element={<PreprocessingDetails/>} />
                  <Route path="/fileSystem" element={<DisplayFileSystem/>}/>
                  <Route path="*" element={<NotFoundPage/>}/>
              </Routes>
          </div>
      </BrowserRouter>
  )
}

export default App
