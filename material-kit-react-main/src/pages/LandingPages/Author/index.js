// @mui material components
//import Card from "@mui/material/Card";

// Material Kit 2 React components
import MKBox from "components/MKBox";
import Box from "@mui/material/Box";
import WarningAmberRoundedIcon from '@mui/icons-material/WarningAmberRounded';

//import Grid from "@mui/material/Grid";
import MKButton from "components/MKButton";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

// Material Kit 2 React examples
import DefaultNavbar from "examples/Navbars/DefaultNavbar";

// Author page sections
//import Profile from "pages/LandingPages/Author/sections/Profile";
//import Posts from "pages/LandingPages/Author/sections/Posts";
//import Contact from "pages/LandingPages/Author/sections/Contact";
import Footer from "pages/LandingPages/Author/sections/Footer";
import CircularProgress from '@mui/material/CircularProgress';

// Routes
import routes from "routes";

// Images
import bgImage from "assets/images/city-profile.jpg";

import { useState, useEffect } from "react";
import MKInput from "components/MKInput";
import MKTypography from "components/MKTypography";
import suggestionsList from './suggestionsList';
import { getAllMessages } from "eventsStore";
import { getApprovedEvents, addApprovedEvent, deleteApprovedEventByName } from "eventsStore";
import { TextField } from "@mui/material"; 

function Author() {
  const [patrolData, setPatrolData] = useState(null);
  const [loading, setLoading] = useState(false);
  //const [month, setMonth] = useState("Month-12");
  const [ward, setWard] = useState("Regent's Park");
  const [filteredSuggestions, setFilteredSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [events, setEvents] = useState([]);
  const [approvedEvents, setApprovedEvents] = useState([]);

  const [selectedDistrict, setSelectedDistrict] = useState("");

  const [newApprovedEvent, setNewApprovedEvent] = useState({
    eventName: "",
    numberOfPeople: "",
    description: "",
  });

  const [scheduleData, setScheduleData] = useState({});
  useEffect(() => {
    if (patrolData?.k) {
      const newScheduleData = {};
      
      // Your strict weekday plan weights (total 56)
      const weekdayWeights = [7, 7, 6, 6, 6, 6, 9, 9];
      const totalWeekdayUnits = weekdayWeights.reduce((a, b) => a + b, 0); // 56

      // Your strict weekend plan weights (assuming you want similar? You can customize)
      const weekendWeights = [6, 7, 7, 7, 7, 6, 10, 10];
      const totalWeekendUnits = weekendWeights.reduce((a, b) => a + b, 0);

      const timeSlots = [
        "06:00 - 08:00",
        "08:00 - 10:00",
        "10:00 - 12:00",
        "12:00 - 14:00",
        "14:00 - 16:00",
        "16:00 - 18:00",
        "18:00 - 20:00",
        "20:00 - 22:00",
      ];

      for (let i = 0; i <= patrolData.k; i++) {
        const normalizedOfficers = {};
        for (const key in patrolData.officers) {
          normalizedOfficers[parseFloat(key)] = patrolData.officers[key];
        }
        //const districtKey = i.toFixed(1);
        //const totalOfficers = patrolData.officers?.[districtKey] ?? 0;
        const totalOfficers = normalizedOfficers[i] ?? 0;
        //(`District ${districtKey} has ${totalOfficers} officers`);
        // Calculate raw allocations as floats
        //console.log(totalOfficers)
        const weekdayAllocations = weekdayWeights.map(weight => (totalOfficers * weight) / totalWeekdayUnits);
        const weekendAllocations = weekendWeights.map(weight => (totalOfficers * weight) / totalWeekendUnits);

        // Floor allocations to integers
        const weekdayFloors = weekdayAllocations.map(Math.floor);
        const weekendFloors = weekendAllocations.map(Math.floor);

        // Calculate leftover officers after flooring
        let weekdayLeftover = totalOfficers - weekdayFloors.reduce((a, b) => a + b, 0);
        let weekendLeftover = totalOfficers - weekendFloors.reduce((a, b) => a + b, 0);

        // Calculate fractional parts to decide where to allocate leftover officers
        const weekdayFractions = weekdayAllocations.map((val, idx) => val - weekdayFloors[idx]);
        const weekendFractions = weekendAllocations.map((val, idx) => val - weekendFloors[idx]);

        // Function to distribute leftover officers based on highest fractions

        const finalWeekdays = distributeLeftover(weekdayFloors, weekdayFractions, weekdayLeftover);
        const finalWeekends = distributeLeftover(weekendFloors, weekendFractions, weekendLeftover);

        // Build schedule for district i
        newScheduleData[i] = timeSlots.map((timeSlot, idx) => ({
          timeSlot,
          weekdays: finalWeekdays[idx],
          weekends: finalWeekends[idx],
        }));
      }

      setScheduleData(newScheduleData);
    }
  }, [patrolData]);

  function distributeLeftover(floors, fractions, leftover) {
    while (leftover > 0) {
      const maxIndex = fractions.indexOf(Math.max(...fractions));
      floors[maxIndex]++;
      fractions[maxIndex] = 0; // Prevent allocating again to the same slot
      leftover--;
    }
    return floors;
  }

  useEffect(() => {
    if (selectedDistrict && patrolData?.k && parseInt(selectedDistrict) > patrolData.k) {
      setSelectedDistrict(""); // Reset if selected district is now invalid
    }
  }, [patrolData, selectedDistrict]);

  useEffect(() => {
    const fetchApproved = async () => {
      const data = await getApprovedEvents();
      setApprovedEvents(data);
    };
    fetchApproved();
  }, []);

  useEffect(() => {
    if (loading) {
      setSelectedDistrict(""); // reset to default when loading starts
    }
  }, [loading]);

  useEffect(() => {
    const fetchEvents = async () => {
      const data = await getAllMessages();
      setEvents(data);
    };

    fetchEvents();
  }, []);

  const handleAddApprovedEvent = async () => {
    if (
      !newApprovedEvent.eventName ||
      !newApprovedEvent.numberOfPeople ||
      !newApprovedEvent.description
    ) {
      alert("Please fill in all fields.");
      return;
    }

    await addApprovedEvent(newApprovedEvent);
    const updated = await getApprovedEvents();
    setApprovedEvents(updated);
    setNewApprovedEvent({ eventName: "", numberOfPeople: "", description: "" });
  };

  const requestPatrolData = async (month, ward) => {
    setLoading(true);
    try {
      const res = await fetch("https://api.streetguard.info/api/patrol", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ month, ward }),
      });
      const result = await res.json();
      if (result.success) {
        return result.data;
      } else {
        console.error("Server Error:", result.error);
      }
    } catch (err) {
      console.error("Network Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const input = e.target.value;
    setWard(input);

    if (input.length > 0) {
      const filtered = suggestionsList.filter((sugg) =>
        sugg.toLowerCase().startsWith(input.toLowerCase())
      );
      setFilteredSuggestions(filtered);
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  };

  const handleSelect = (suggestion) => {
    setWard(suggestion);
    setShowSuggestions(false);
  };

  const handleSubmit = async () => {
    const data = await requestPatrolData("Month-12", ward);
    if (data) setPatrolData(data);
  };

  const downloadImage = (base64Image, filename = 'map.png') => {
    const link = document.createElement('a');
    link.href = `data:image/png;base64,${base64Image}`;
    link.download = filename;
    link.click();
  };

  const isValidWard = suggestionsList.includes(ward);

  return (
    <>
      <MKBox position="fixed" top="0.5rem" width="100%">
        <DefaultNavbar routes={routes} />
      </MKBox>

      <MKBox bgColor="white">
        <MKBox
          minHeight="25rem"
          width="100%"
          sx={{
            backgroundImage: ({ functions: { linearGradient, rgba }, palette: { gradients } }) =>
              `${linearGradient(
                rgba(gradients.dark.main, 0.8),
                rgba(gradients.dark.state, 0.8)
              )}, url(${bgImage})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            display: "grid",
            placeItems: "center",
          }}
        >
          <MKTypography variant="h2" color="white" fontWeight="bold">
            Patrol Data Viewer
          </MKTypography>
        </MKBox>
        <MKBox p={2} px={26}>
          <Accordion
            style={{
              border: "1.5px solid #ccc",
              borderRadius: "16px",
              boxShadow: "0 12px 32px rgba(0, 0, 0, 0.1)",
              marginBottom: "1.5rem",
              padding: "0.5rem",
            }}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="how-to-use-content"
              id="how-to-use-header"
            >
              <MKTypography variant="h6">How to Use</MKTypography>
            </AccordionSummary>
            <AccordionDetails>
              <MKTypography variant="body2">
                - Type a ward name in the input field.<br />
                - Select a suggestion from the dropdown if applicable.<br />
                - Click to display the map and officers.<br />
                - Scroll to view officer distribution and map.<br />
                - Use the download button to save the map image.<br />
                - Select a district in the patrol schedule to view officer allocation per time slot.<br />
                - The left table in the Special Operations Events shows proposal events from people.<br />
                - The right table in the Special Operations Events shows approved events for special operations.<br />
                - Filling the form in Special Operations Events adds an event to the approved section.<br />
                - To delete an approved operation type only the name of the event and press the delete button.<br />
              </MKTypography>
            </AccordionDetails>
          </Accordion>
        </MKBox>
        <MKBox p={2} px={26} py={2}>
          <Paper
            elevation={0}
            style={{
              border: "1.5px solid #ccc",
              borderRadius: "16px",
              padding: "1.5rem",
              boxShadow: "0 12px 32px rgba(0, 0, 0, 0.1)",
            }}
          >
            <MKBox display="flex" alignItems="center" flexWrap="wrap" gap={2}>
              {/* Search Input */}
              <div style={{ position: 'relative', flex: 1, minWidth: 250 }}>
                <MKInput
                  type="text"
                  label="Ward"
                  value={ward}
                  onChange={handleChange}
                  placeholder="e.g. Regent's Park"
                  style={{ width: '100%' }}
                  varient="standard"
                />
                {showSuggestions && (
                  <ul
                    style={{
                      position: 'absolute',
                      backgroundColor: 'white',
                      border: '1px solid #ccc',
                      listStyle: 'none',
                      padding: 0,
                      marginTop: '5px',
                      width: '100%',
                      zIndex: 10,
                      maxHeight: '150px',
                      overflowY: 'auto',
                      borderRadius: '4px',
                    }}
                  >
                    {filteredSuggestions.map((sugg, index) => (
                      <li
                        key={index}
                        onClick={() => handleSelect(sugg)}
                        style={{
                          padding: '8px',
                          cursor: 'pointer',
                          borderBottom: '1px solid #eee',
                        }}
                      >
                        {sugg}
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              {/* Load Button */}
              <MKButton
                variant="gradient"
                color="info"
                onClick={handleSubmit}
                disabled={loading || !isValidWard}
                style={{ whiteSpace: "nowrap", height: "fit-content", marginTop: "0rem"}}
              >
                {loading ? "Loading..." : "Load Patrol Data"}
              </MKButton>
              {patrolData?.map_image && (
                <MKButton
                  variant="gradient"
                  color="info"
                  onClick={() =>
                    downloadImage(
                      patrolData.map_image,
                      `${ward.replace(/\s+/g, "_")}_patrol_map.png`
                    )
                  }
                  style={{ marginTop: "0rem", whiteSpace: "nowrap", height: "fit-content"}}
                  disabled={loading || !isValidWard}
                >
                  Download Map
                </MKButton>
              )}
            </MKBox>
            {ward && !isValidWard && (
              <MKBox>
                <MKTypography variant="caption" color="error">
                  Please select a valid ward from the list.
                </MKTypography>
              </MKBox>
            )}
            {/* Total Districts Text */}
            {patrolData && (
              <Box
                mt={3}
                mb={1}
                px={3}
                py={1}
                borderRadius={2}
                bgcolor="background.paper"
                border="1px solid #ccc"
                display="inline-block"
              >
                <MKTypography 
                  variant="subtitle2" 
                  fontWeight={500} 
                  color="text.secondary" 
                  letterSpacing={0.5}
                >
                  Total Patrol Districts: <strong>{patrolData.k}</strong>
                </MKTypography>
              </Box>
            )}
            <MKBox mt={2} display="flex" alignItems="center" gap={1}>
              <WarningAmberRoundedIcon fontSize="small" color="warning" />
                <MKTypography 
                  variant="caption" 
                  color="text.secondary"
                  fontStyle="italic"
                  lineHeight={1.5}
                >
                  Advisory only. Please interpret with care and consideration.
                </MKTypography>
            </MKBox>
          </Paper>
        </MKBox>
        <MKBox p={2}>
            {patrolData && (
              <>
                <MKBox display="flex" gap={2} flexWrap="wrap" px={24} py={5}>
                  {/* Map Image */}
                  <MKBox flex="3">
                    {/*}
                    <img
                      src={`data:image/png;base64,${patrolData.map_image}`}
                      alt="Map"
                      style={{ width: "100%", height: "auto" }}
                    />
                    */}
                    <Paper
                      elevation={0} // no shadow
                      style={{
                        border: "1.5px solid #ccc", // thin solid border
                        borderRadius: "16px",       // rounded corners (oval-ish)
                        padding: "0.5rem",           // inner spacing
                        boxShadow: "0 12px 32px rgba(0, 0, 0, 0.1)",
                      }}
                    >
                      {loading ? (
                        <MKBox
                          display="flex"
                          justifyContent="center"
                          alignItems="center"
                          height="100%"
                          minHeight="285px"
                        >
                          <CircularProgress />
                        </MKBox>
                      ) : (
                        <img
                        src={`data:image/png;base64,${patrolData.map_image}`}
                        alt="Map"
                        style={{ width: "100%", height: "auto", display: "block", borderRadius: "12px" }}
                      />
                      )}
                    </Paper>
                  </MKBox>
                  {/* District Officer Counts Table */}
                  <MKBox flex="1">
                    <TableContainer
                      component={Paper}
                      style={{
                        border: "1.5px solid #ccc",          // custom single border
                        borderRadius: "16px",                // rounded corners
                        boxShadow: "0 12px 32px rgba(0, 0, 0, 0.1)", // shadow
                        minHeight: "300px",                  // maintain height during loading
                      }}
                    >
                      {loading ? (
                        <MKBox
                          display="flex"
                          justifyContent="center"
                          alignItems="center"
                          height="100%"
                          minHeight="300px"
                        >
                          <CircularProgress />
                        </MKBox>
                      ) : (
                        <Table>
                        <TableHead>
                        </TableHead>
                        <TableBody>
                          <TableRow>
                            <TableCell
                              align="center"
                              sx={{
                                width: '50%',
                                textAlign: 'center',
                                verticalAlign: 'middle',
                                padding: '12px',
                              }}
                            >
                              <strong>District ID</strong>
                            </TableCell>
                            <TableCell
                              align="center"
                              sx={{
                                width: '50%',
                                textAlign: 'center',
                                verticalAlign: 'middle',
                                padding: '12px',
                              }}
                            >
                              <strong>Number of Officers</strong>
                            </TableCell>
                          </TableRow>
                          {Object.entries(patrolData.officers || {}).map(([district, count]) => (
                            <TableRow key={district}>
                              <TableCell
                                align="right"
                                sx={{ textAlign: "center", verticalAlign: "middle", padding: "12px" }}
                              >
                                {parseInt(district)}
                              </TableCell>
                              <TableCell
                                align="left"
                                sx={{ textAlign: "center", verticalAlign: "middle", padding: "12px" }}
                              >
                                {count}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                      )}
                    </TableContainer>
                  </MKBox>
                </MKBox>
              </>
            )}
            {patrolData && (
              <MKBox px={26} mt={4}>
                <Paper
                  elevation={0}
                  style={{
                    border: "1.5px solid #ccc",
                    borderRadius: "16px",
                    padding: "1.5rem",
                    boxShadow: "0 12px 32px rgba(0, 0, 0, 0.1)",
                  }}
                >
                  <MKTypography variant="h6" mb={2}>
                    Patrol Schedule by District
                  </MKTypography>

                  {/* Dropdown */}
                  <TextField
                    select
                    value={selectedDistrict}
                    onChange={(e) => setSelectedDistrict(e.target.value)}
                    SelectProps={{ native: true }}
                    variant="outlined"
                    fullWidth
                    sx={{ mb: 3 }}
                    disabled={loading}
                  >
                    <option value="" disabled>Select a district</option>
                    {Array.from({ length: patrolData.k }, (_, i) => (
                      <option key={i} value={i}>
                        District {i}
                      </option>
                    ))}
                  </TextField>

                  {/* Schedule Table */}
                  {selectedDistrict && (
                    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
                      <Table>
                        <TableHead>
                        </TableHead>
                        <TableBody>
                        {loading ? (
                          <TableRow>
                            <TableCell colSpan={3} align="center" sx={{ py: 4 }}>
                              <CircularProgress size={32} />
                              <MKTypography variant="body2" mt={2}>
                                Loading schedule data...
                              </MKTypography>
                            </TableCell>
                          </TableRow>
                        ) : (
                          <>
                            <TableRow>
                              <TableCell><strong>Time Slot</strong></TableCell>
                              <TableCell><strong>Weekdays (Shifts)</strong></TableCell>
                              <TableCell><strong>Weekends (Shifts)</strong></TableCell>
                            </TableRow>
                            {(scheduleData[selectedDistrict] || []).map((row, index) => (
                              <TableRow key={index}>
                                <TableCell>{row.timeSlot}</TableCell>
                                <TableCell>{row.weekdays}</TableCell>
                                <TableCell>{row.weekends}</TableCell>
                              </TableRow>
                            ))}
                          </>
                        )}
                      </TableBody>
                      </Table>
                    </TableContainer>
                  )}
                </Paper>
              </MKBox>
            )}
        </MKBox>
        <MKBox px={26} py={2}>
          <Paper
            elevation={0}
            style={{
              border: "1.5px solid #ccc",
              borderRadius: "16px",
              padding: "1.5rem",
              boxShadow: "0 12px 32px rgba(0, 0, 0, 0.1)",
            }}
          >
            <MKTypography variant="h5" mb={2}>
              Special Operations Events
            </MKTypography>

              <MKBox display="flex" gap={4}>
                {/* Submitted Events Table */}
                <TableContainer
                  component={Paper}
                  style={{
                    borderRadius: "12px",
                    maxHeight: "200px",
                    overflowY: "auto",
                    width: "60%",
                  }}
                >
                  <Table style={{ tableLayout: "fixed", width: "100%", borderCollapse: "collapse" }}>
                    {/*}
                    <TableHead>
                      <TableRow style={{ width: "200%", }}>
                        <TableCell style={{ borderRight: "1px solid #ccc", width: "200%", }}><strong>Proposals</strong></TableCell>
                        <TableCell style={{ borderRight: "1px solid #ccc", width: "200%",}}><strong># of People</strong></TableCell>
                        <TableCell style={{ width: "200%",}}><strong>Description</strong></TableCell>
                      </TableRow>
                    </TableHead>
                    */}
                    <TableBody>
                      <TableRow style={{ width: "200%", }}>
                        <TableCell style={{ borderRight: "1px solid #ccc", width: "200%", }}><strong>Proposals</strong></TableCell>
                        <TableCell style={{ borderRight: "1px solid #ccc", width: "200%",}}><strong># of People</strong></TableCell>
                        <TableCell style={{ width: "200%",}}><strong>Description</strong></TableCell>
                      </TableRow>
                      {events.map((event, index) => (
                        <TableRow key={index}>
                          <TableCell style={{ borderRight: "1px solid #eee" }}>{event.eventName}</TableCell>
                          <TableCell style={{ borderRight: "1px solid #eee" }}>{event.numberOfPeople}</TableCell>
                          <TableCell style={{  }}>{event.description}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>

                {/* Approved Events Table */}
                <TableContainer
                  component={Paper}
                  style={{
                    borderRadius: "12px",
                    maxHeight: "200px",
                    overflowY: "auto",
                    width: "60%",
                  }}
                >
                  <Table style={{ tableLayout: "fixed", width: "100%", borderCollapse: "collapse" }}>
                    {/*}
                    <TableHead>
                      <TableRow>
                        <TableCell style={{ borderRight: "1px solid #ccc" }}><strong>Approved</strong></TableCell>
                        <TableCell style={{ borderRight: "1px solid #ccc" }}><strong># of People</strong></TableCell>
                        <TableCell><strong>Description</strong></TableCell>
                      </TableRow>
                    </TableHead>
                    */}
                    <TableBody>
                      <TableRow>
                        <TableCell style={{ borderRight: "1px solid #ccc" }}><strong>Approved</strong></TableCell>
                        <TableCell style={{ borderRight: "1px solid #ccc" }}><strong># of People</strong></TableCell>
                        <TableCell><strong>Description</strong></TableCell>
                      </TableRow>
                      {approvedEvents.map((event, index) => (
                        <TableRow key={index}>
                          <TableCell style={{ width: "33.33%", borderRight: "1px solid #eee" }}>{event.eventName}</TableCell>
                          <TableCell style={{ width: "33.33%", borderRight: "1px solid #eee" }}>{event.numberOfPeople}</TableCell>
                          <TableCell style={{ width: "33.33%" }}>{event.description}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
                <MKBox mt={2} display="flex" flexDirection="column" gap={2} width="50%">
                  <TextField
                    label="Event Name"
                    value={newApprovedEvent.eventName}
                    onChange={(e) => setNewApprovedEvent({ ...newApprovedEvent, eventName: e.target.value })}
                    fullWidth
                  />
                  <TextField
                    label="# of People"
                    value={newApprovedEvent.numberOfPeople}
                    onChange={(e) => setNewApprovedEvent({ ...newApprovedEvent, numberOfPeople: e.target.value })}
                    fullWidth
                    type="number"
                  />
                  <TextField
                    label="Description"
                    value={newApprovedEvent.description}
                    onChange={(e) => setNewApprovedEvent({ ...newApprovedEvent, description: e.target.value })}
                    fullWidth
                    multiline
                    rows={2}
                  />
                  <MKButton variant="gradient" color="info" onClick={handleAddApprovedEvent}>
                    Add Approved Event
                  </MKButton>
                  <MKButton
                    color="error"
                    variant="gradient"
                    onClick={async () => {
                      await deleteApprovedEventByName(newApprovedEvent.eventName); // Call the Firestore delete
                      const updated = await getApprovedEvents(); // Refresh UI
                      setApprovedEvents(updated);
                    }}
                  >
                    Delete Approved Event
                  </MKButton>
                 </MKBox>
                </MKBox>
            </Paper>
        </MKBox>
        <Footer />
      </MKBox>
    </>
  );
}

export default Author;
