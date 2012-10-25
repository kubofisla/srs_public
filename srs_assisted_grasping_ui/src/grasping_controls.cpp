/******************************************************************************
 * \file
 *
 * $Id:$
 *
 * Copyright (C) Brno University of Technology
 *
 * This file is part of software developed by dcgm-robotics@FIT group.
 *
 * Author: Zdenek Materna (imaterna@fit.vutbr.cz)
 * Supervised by: Michal Spanel (spanel@fit.vutbr.cz)
 * Date: 5/4/2012
 * 
 * This file is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This file is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License
 * along with this file.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <srs_assisted_grasping_ui/grasping_controls.h>

#include <rviz/window_manager_interface.h>

using namespace std;
using namespace srs_assisted_grasping_ui;
using namespace srs_assisted_grasping_msgs;
using namespace srs_assisted_grasping;

const int ID_BUTTON_GRASP(101);
const int ID_BUTTON_STOP(102);
const int ID_SLIDER_FORCE(104);

const int ID_CHOICE(115);

const int ID_SLIDER_FORCE_1(105);
const int ID_SLIDER_FORCE_2(106);
const int ID_SLIDER_FORCE_3(107);

/*
 * TODO
 *
 *  - subscribe for tactile data and visualize it (all the time)
 *  - add groups "Object grasping", "Force feedback"
 *  - add combobox for presets, hardcode some
 *  - read grasping presets from YAML
 *
 */

/**
 Constructor
 */
CButGraspingControls::CButGraspingControls(wxWindow *parent, const wxString& title, rviz::WindowManagerInterface * wmi )
    : wxPanel( parent, wxID_ANY, wxDefaultPosition, wxSize(280, 180), wxTAB_TRAVERSAL, title)
    , m_wmi( wmi )
{

    parent_ = parent;

    ros::param::param<double>("~abs_max_force", abs_max_force_ , ABS_MAX_FORCE);
    ros::param::param<bool>("~wait_for_allow", wait_for_allow_ , WAIT_FOR_ALLOW);

    // TODO read presets from yaml
    Preset pr;
    pr.name = "Empty bottle";
    pr.forces.resize(6);

    for(int i=0; i < 6; i++) pr.forces[i] = 300.0;

    pr.target_pos.resize(7);

    pr.target_pos[0] = 0.0;
    pr.target_pos[1] = 0.0;
    pr.target_pos[2] = 1.0472;
    pr.target_pos[3] = 0.0;
    pr.target_pos[4] = 1.0472;
    pr.target_pos[5] = 0.0;
    pr.target_pos[6] = 1.0472;

    pr.time = ros::Duration(5.0);

    presets_.push_back(pr);

    wxArrayString prt;

    for(unsigned int i=0; i < presets_.size(); i++)
    	prt.Add(wxString::FromAscii(presets_[i].name.c_str()));

    presets_choice_ = new wxChoice(this, ID_CHOICE,wxDefaultPosition,wxDefaultSize,prt);

    buttons_["grasp"] = new wxButton(this, ID_BUTTON_GRASP, wxT("Grasp"),wxDefaultPosition,wxDefaultSize,wxBU_EXACTFIT);
    buttons_["stop"] = new wxButton(this, ID_BUTTON_STOP, wxT("Stop"),wxDefaultPosition,wxDefaultSize,wxBU_EXACTFIT);

    m_text_status_ = new wxStaticText(this, -1, wxT("status: idle"));

    stringstream ss (stringstream::in | stringstream::out);

    ss << "max. force: ";
    ss << abs_max_force_/2.0;

    string tmp = ss.str();

    m_text_max_force_ = new wxStaticText(this, -1, wxString::FromAscii(tmp.c_str()));

    max_force_slider_ = new wxSlider(this,ID_SLIDER_FORCE,abs_max_force_/2.0,0,abs_max_force_,wxDefaultPosition,wxDefaultSize,wxSL_LABELS);

    finger1_force_slider_ = new wxSlider(this,ID_SLIDER_FORCE_1,0.0,0,abs_max_force_);
    finger2_force_slider_ = new wxSlider(this,ID_SLIDER_FORCE_2,0.0,0,abs_max_force_);
    finger3_force_slider_ = new wxSlider(this,ID_SLIDER_FORCE_3,0.0,0,abs_max_force_);

    tactile_data_.resize(6);

    wxSizer *hsizer_buttons = new wxBoxSizer(wxHORIZONTAL);



    hsizer_buttons->Add(buttons_["grasp"], ID_BUTTON_GRASP);
    hsizer_buttons->Add(buttons_["stop"], ID_BUTTON_STOP);

    wxSizer *vsizer = new wxBoxSizer(wxVERTICAL); // top sizer

    vsizer->Add(hsizer_buttons);



    vsizer->Add(m_text_status_);
    vsizer->Add(m_text_max_force_);

    vsizer->Add(presets_choice_);

    wxSizer *vsizer_sliders = new wxStaticBoxSizer(wxVERTICAL,this,wxT("Force feedback"));

    vsizer_sliders->Add(max_force_slider_,1,wxEXPAND);

    vsizer_sliders->Add(finger1_force_slider_,1,wxEXPAND);
    vsizer_sliders->Add(finger2_force_slider_,1,wxEXPAND);
    vsizer_sliders->Add(finger3_force_slider_,1,wxEXPAND);

    vsizer->Add(vsizer_sliders,1,wxEXPAND);


    finger1_force_slider_->Enable(false);
    finger2_force_slider_->Enable(false);
    finger3_force_slider_->Enable(false);

    setButton("stop",false);

    grasping_allowed_ = false;

    if (wait_for_allow_) {

    	DisableControls();

    } else {

    	EnableControls();
    }

    Connect(ID_SLIDER_FORCE, wxEVT_SCROLL_THUMBRELEASE,
              wxCommandEventHandler(CButGraspingControls::OnMaxForceSlider));

    vsizer->SetSizeHints(this);
    this->SetSizerAndFit(vsizer);

    as_client_ = new grasping_action_client(ACT_GRASP,true);

    ros::NodeHandle nh;

    tactile_data_received_ = false;

    stop_gui_thread_ = false;

    t_gui_update = boost::thread(&CButGraspingControls::GuiUpdateThread,this);

    //gui_update_timer_ = nh.createTimer(ros::Duration(0.5),&CButGraspingControls::timerCallback,this);

    tact_sub_  = nh.subscribe("/sdh_controller/tactile_data_filtered", 10, &CButGraspingControls::TactileDataCallback,this);

    service_grasping_allow_ = nh.advertiseService(SRV_ALLOW,&CButGraspingControls::GraspingAllow,this);


}

void CButGraspingControls::GuiUpdateThread() {

	ROS_INFO("Grasping GUI thread started.");

	ros::Rate r(10);

	while(!stop_gui_thread_) {

		if (tactile_data_received_) {

			std::vector<int16_t> tmp;

			tactile_data_mutex_.lock();

			tmp = tactile_data_;

			tactile_data_mutex_.unlock();

			wxMutexGuiEnter();

			if (tmp[0] > tmp[1] ) finger1_force_slider_->SetValue(tmp[0]);
			else finger1_force_slider_->SetValue(tmp[1]);

			if (tmp[2] > tmp[3] ) finger2_force_slider_->SetValue(tmp[2]);
			else finger2_force_slider_->SetValue(tmp[3]);

			if (tmp[4] > tmp[5] ) finger3_force_slider_->SetValue(tmp[4]);
			else finger3_force_slider_->SetValue(tmp[5]);

			wxMutexGuiLeave();

		}

		r.sleep();

	}

	stop_gui_thread_ = false;


}

void CButGraspingControls::TactileDataCallback(const schunk_sdh::TactileSensor::ConstPtr& msg) {

  ROS_INFO_ONCE("Tactile data received.");

  tactile_data_mutex_.lock();

  // for each pad find the maximum value
  for(unsigned int i=0; i < 6; i++) {

	  int16_t max = 0;

	  for (unsigned int j=0; j < (unsigned int)(msg->tactile_matrix[i].cells_x*msg->tactile_matrix[i].cells_y); j++) {

		  if ( (msg->tactile_matrix[i].tactile_array[j] > max) && (msg->tactile_matrix[i].tactile_array[j] < 20000) ) max = msg->tactile_matrix[i].tactile_array[j];

	  }

	  tactile_data_[i] = max;

  }

  tactile_data_received_ = true;

  tactile_data_mutex_.unlock();


}



void CButGraspingControls::setButton(string but, bool state) {

  if (buttons_[but]!=NULL)
    buttons_[but]->Enable(state);

}


CButGraspingControls::~CButGraspingControls() {

  stop_gui_thread_ = true;

  ros::Rate r(0.1);

  while(stop_gui_thread_ == true) r.sleep();

  ButtonsMap::iterator it;

    for (it = buttons_.begin(); it != buttons_.end(); ++it)
      delete it->second;

    buttons_.clear();

    delete as_client_;


}


void CButGraspingControls::GraspingThread() {

  ROS_INFO("Let's start grasping...");

  if (!as_client_->waitForServer(ros::Duration(3.0))) {

    ROS_ERROR("Grasping action server not running!");

    wxMutexGuiEnter();
    m_text_status_->SetLabel(wxString::FromAscii("status: Communication error."));

    EnableControls();

    wxMutexGuiLeave();

    return;

  }

  int choice = presets_choice_->GetSelection();

  ReactiveGraspingGoal goal;

  goal.target_configuration.data.resize(presets_[choice].target_pos.size());
  goal.max_force.data.resize(presets_[choice].forces.size());

  for (unsigned int i=0; i < presets_[choice].target_pos.size(); i++)
	  goal.target_configuration.data[i] = presets_[choice].target_pos[i];

  for (unsigned int i=0; i < presets_[choice].forces.size(); i++)
  	  goal.max_force.data[i] = presets_[choice].forces[i];

  //goal.target_configuration.data = presets_[choice].target_pos;
  //goal.max_force.data = presets_[choice].forces;

  goal.time = presets_[choice].time;

  grasping_finished_ = false;

  as_client_->sendGoal(goal,
		  boost::bind(&CButGraspingControls::GraspingDone, this, _1, _2),
		  boost::bind(&CButGraspingControls::GraspingActive, this));


  // TODO timeout!!!!!!!!!!!!!! treat case if action fails.....

  uint16_t i=0;

  ros::Duration dur(1);

  // wait for 60 seconds
  while( (i < 60) && (!grasping_finished_) ) {

	  dur.sleep();

  }

  if (!grasping_finished_) {

	  ROS_ERROR("Manual grasping action timeouted.");

	  wxMutexGuiEnter();
	  m_text_status_->SetLabel(wxString::FromAscii("status: Timeout."));

	  setButton("stop",false);

	  if (grasping_allowed_ || !wait_for_allow_) {

		  EnableControls();

	  }

	  wxMutexGuiLeave();

	  as_client_->cancelAllGoals();

  }

  return;


}


void CButGraspingControls::GraspingDone(const actionlib::SimpleClientGoalState& state,
					  const ReactiveGraspingResultConstPtr& result) {

	ROS_INFO("Grasping action finished...");

	grasping_finished_ = true;

	wxMutexGuiEnter();

	  if (state == actionlib::SimpleClientGoalState::SUCCEEDED) {


	    ROS_INFO("Object should be now grasped.");
	    m_text_status_->SetLabel(wxString::FromAscii("status: Grasping completed."));

	  } else {

	    ROS_ERROR("Grasping failed.");
	    m_text_status_->SetLabel(wxString::FromAscii("status: Grasping failed."));

	  }

	  if (grasping_allowed_ || !wait_for_allow_) {

		  EnableControls();

	      }

	  setButton("stop",false);

	  /*finger1_force_slider_->SetValue(0);
	  finger2_force_slider_->SetValue(0);
	  finger3_force_slider_->SetValue(0);*/

	  wxMutexGuiLeave();

}

void CButGraspingControls::OnStop(wxCommandEvent& event) {

  as_client_->cancelAllGoals();

  if (grasping_allowed_ || !wait_for_allow_) {

	  EnableControls();

  } else {

	  DisableControls();

  }

}

void CButGraspingControls::EnableControls() {

	setButton("grasp",true);
	max_force_slider_->Enable(true);


}

void CButGraspingControls::DisableControls(bool state_of_stop_button) {

	setButton("grasp",false);
	max_force_slider_->Enable(false);

	setButton("stop",state_of_stop_button);


}

void CButGraspingControls::OnGrasp(wxCommandEvent& event) {

  boost::posix_time::time_duration td = boost::posix_time::milliseconds(100);

  /// wait for some time
  if (t_grasping.timed_join(td)) {

    m_text_status_->SetLabel(wxString::FromAscii("status: Trying to grasp. Please wait..."));

    //wxMutexGuiEnter();
    DisableControls(true);
    //wxMutexGuiLeave();

    t_grasping = boost::thread(&CButGraspingControls::GraspingThread,this);

  } else ROS_INFO("We have to wait until GRASPING thread finishes.");


}

void CButGraspingControls::OnMaxForceSlider(wxCommandEvent& event) {

  stringstream ss (stringstream::in | stringstream::out);

  ss << "max. force: ";
  ss << (double)max_force_slider_->GetValue();

  string tmp = ss.str();

  m_text_max_force_->SetLabel(wxString::FromAscii(tmp.c_str()));


}

bool CButGraspingControls::GraspingAllow(GraspingAllow::Request &req, GraspingAllow::Response &res) {


	if (req.allow) {

		ROS_INFO("Grasping: enabling controls.");

		//wxMutexGuiEnter();
		EnableControls();
		//wxMutexGuiLeave();

		grasping_allowed_ = true;

	} else {

		ROS_INFO("Grasping: disabling controls.");

		//wxMutexGuiEnter();
		DisableControls();
		//wxMutexGuiLeave();

		grasping_allowed_ = false;

	}


	return true;

}


BEGIN_EVENT_TABLE(CButGraspingControls, wxPanel)
    EVT_BUTTON(ID_BUTTON_GRASP,  CButGraspingControls::OnGrasp)
    EVT_BUTTON(ID_BUTTON_STOP,  CButGraspingControls::OnStop)
END_EVENT_TABLE()

