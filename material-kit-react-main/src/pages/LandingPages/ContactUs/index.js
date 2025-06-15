// @mui material components
import Grid from "@mui/material/Grid";
import React, { useState } from "react";
import ReCAPTCHA from "react-google-recaptcha";
import { useRef } from "react";

// Material Kit 2 React components
import MKBox from "components/MKBox";
import MKInput from "components/MKInput";
import MKButton from "components/MKButton";
import MKTypography from "components/MKTypography";

// Material Kit 2 React examples
import DefaultNavbar from "examples/Navbars/DefaultNavbar";
import DefaultFooter from "examples/Footers/DefaultFooter";

// Routes
import routes from "routes";
import footerRoutes from "footer.routes";
import { addEvent } from "eventsStore"; // Adjust path if needed

// Image
import bgImage from "assets/images/illustrations/illustration-reset.jpg";

function ContactUs() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });

  const [eventData, setEventData] = useState({
    eventName: "",
    numberOfPeople: "",
    description: "",
  });
  //const [submittedEvents, setSubmittedEvents] = useState([]);
  const recaptchaRef = useRef(null);
  const [captchaValue, setCaptchaValue] = useState(null);

  const handleEventChange1 = (e) => {
  const { name, value } = e.target;
    setEventData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  {/*}
  const handleEventSubmit1 = async (e) => {
    e.preventDefault();
    try {
      await addEvent(eventData); // ✅ Save to Firestore
      console.log("Event submitted:", eventData);
      setEventData({ eventName: "", numberOfPeople: "", description: "" });
    } catch (error) {
      console.error("Failed to submit event:", error);
    }
  };
  */}
  const handleEventSubmit1 = async (e) => {
    e.preventDefault();

    if (!captchaValue) {
      alert("Please verify that you are not a robot.");
      return;
    }

    try {
      // Optionally, you can verify captchaValue on your backend here before calling addEvent

      await addEvent(eventData);
      //console.log("Event submitted:", eventData);
      setEventData({ eventName: "", numberOfPeople: "", description: "" });
      setCaptchaValue(null);
      recaptchaRef.current.reset();
    } catch (error) {
      console.error("Failed to submit event:", error);
    }
  };
  const [messages, setMessages] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Add the current form data to the messages array
    setMessages((prevMessages) => [...prevMessages, formData]);

    // Optional: Console log for debugging
    //console.log("All Messages:", [...messages, formData]);
    messages.sort()
    // Reset form
    setFormData({
      name: "",
      email: "",
      message: "",
    });
  };

  return (
    <>
      <MKBox position="fixed" top="0.5rem" width="100%">
        <DefaultNavbar routes={routes} />
      </MKBox>
      <Grid container spacing={3} alignItems="center">
        <Grid item xs={12} lg={6}>
          <MKBox
            display={{ xs: "none", lg: "flex" }}
            width="calc(100% - 2rem)"
            height="calc(100vh - 2rem)"
            borderRadius="lg"
            ml={2}
            mt={2}
            sx={{ backgroundImage: `url(${bgImage})` }}
          />
        </Grid>
        <Grid
          item
          xs={12}
          sm={10}
          md={7}
          lg={6}
          xl={4}
          ml={{ xs: "auto", lg: 6 }}
          mr={{ xs: "auto", lg: 6 }}
        >
          <MKBox
            bgColor="white"
            borderRadius="xl"
            shadow="lg"
            display="flex"
            flexDirection="column"
            justifyContent="center"
            mt={{ xs: 20, sm: 18, md: 20 }}
            mb={{ xs: 20, sm: 18, md: 20 }}
            mx={3}
          >
            <MKBox
              variant="gradient"
              bgColor="info"
              coloredShadow="info"
              borderRadius="lg"
              p={2}
              mx={2}
              mt={-3}
            >
              <MKTypography variant="h3" color="white">
                Contact us
              </MKTypography>
            </MKBox>
            <MKBox p={3}>
              <MKTypography variant="body2" color="text" mb={3}>
              </MKTypography>
              <MKBox width="100%" component="form" method="post" autoComplete="off" onSubmit={handleSubmit}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <MKInput
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      variant="standard"
                      label="Full Name"
                      InputLabelProps={{ shrink: true }}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <MKInput
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      variant="standard"
                      label="Email"
                      InputLabelProps={{ shrink: true }}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <MKInput
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      variant="standard"
                      label="What can we help you?"
                      placeholder="Describe your message here..."
                      InputLabelProps={{ shrink: true }}
                      multiline
                      fullWidth
                      rows={6}
                    />
                  </Grid>
                </Grid>
                <Grid container item justifyContent="center" xs={12} mt={5} mb={2}>
                  <MKButton type="submit" variant="gradient" color="info">
                    Send Message
                  </MKButton>
                </Grid>
              </MKBox>
            </MKBox>
            <MKBox
                variant="gradient"
                bgColor="info"
                coloredShadow="info"
                borderRadius="lg"
                p={2}
                mx={2}
                mt={-3}
              >
                <MKTypography variant="h3" color="white">
                  Event Report
                </MKTypography>
              </MKBox>
            <MKBox mt={5} p={3}>
              <MKBox component="form" onSubmit={handleEventSubmit1} mt={2}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <MKInput
                      name="eventName"
                      value={eventData.eventName}
                      onChange={handleEventChange1}
                      variant="standard"
                      label="Name of Event"
                      InputLabelProps={{ shrink: true }}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <MKInput
                      name="numberOfPeople"
                      type="number"
                      value={eventData.numberOfPeople}
                      onChange={handleEventChange1}
                      variant="standard"
                      label="Number of People"
                      InputLabelProps={{ shrink: true }}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <MKInput
                      name="description"
                      value={eventData.description}
                      onChange={handleEventChange1}
                      variant="standard"
                      label="Brief Description"
                      placeholder="Describe the event..."
                      InputLabelProps={{ shrink: true }}
                      multiline
                      rows={4}
                      fullWidth
                    />
                  </Grid>
                </Grid>
                <Grid container justifyContent="center" mt={3} mb={2}>
                  <ReCAPTCHA
                    sitekey="6LedGl4rAAAAAFD41YRu6DwPFtSxJu4z3fp5HPbs"
                    onChange={(value) => setCaptchaValue(value)}
                    ref={recaptchaRef}
                  />
                </Grid>
                <Grid container item justifyContent="center" xs={12} mt={4}>
                  <MKButton type="submit" variant="gradient" color="info">
                    Send Event Info
                  </MKButton>
                </Grid>
              </MKBox>
            </MKBox>
          </MKBox>
        </Grid>
      </Grid>
      <MKBox pt={6} px={1} mt={6}>
        <DefaultFooter content={footerRoutes} />
      </MKBox>
    </>
  );
}

export default ContactUs;
