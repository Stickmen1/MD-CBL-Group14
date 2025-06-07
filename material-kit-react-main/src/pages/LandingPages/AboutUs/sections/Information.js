// @mui material components
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";

// Material Kit 2 React components
import MKBox from "components/MKBox";
import MKTypography from "components/MKTypography";

// Material Kit 2 React examples
import DefaultInfoCard from "examples/Cards/InfoCards/DefaultInfoCard";
//import CenteredBlogCard from "examples/Cards/BlogCards/CenteredBlogCard";

function Information() {
  return (
    <MKBox component="section" py={5}>
      <Container>
        <Grid item xs={12} md={8} sx={{ mb: 4 }}>
          <MKTypography variant="h3" color="black">
            Our Missions
          </MKTypography>
      </Grid>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} lg={12}>
            <Grid container justifyContent="flex-start">
              <Grid item xs={12} md={6}>
                <MKBox mb={5} 
                sx={{
                  p: 2, // smaller padding
                  width: "100%", // or set a fixed width like '300px'
                  maxWidth: "75%", // optional max width
                  backgroundColor: "#e3f2fd", // light blue background
                  border: "1px solid #0d3f8f", // blue border
                  borderRadius: 2,
                  transition: "all 0.3s ease",
                  "&:hover": {
                    boxShadow: 8,
                    backgroundColor: "#bbdefb", // slightly darker blue on hover
                  },
                }}
                >
                  <DefaultInfoCard
                    icon="poll"
                    title="Data Empowerment"
                    description="Empower London&apos;s police with data-driven insights."
                  />
                </MKBox>
              </Grid>
              <Grid item xs={12} md={6}>
                <MKBox mb={5}
                sx={{
                  p: 2, // smaller padding
                  width: "100%", // or set a fixed width like '300px'
                  maxWidth: "75%", // optional max width
                  backgroundColor: "#e3f2fd", // light blue background
                  border: "1px solid #0d3f8f", // blue border
                  borderRadius: 2,
                  transition: "all 0.3s ease",
                  "&:hover": {
                    boxShadow: 8,
                    backgroundColor: "#bbdefb", // slightly darker blue on hover
                  },
                }}
                >
                  <DefaultInfoCard
                    icon="security"
                    title="Proactive Prevention"
                    description="Predict and prevent burglaries before they happen."
                  />
                </MKBox>
              </Grid>
              <Grid item xs={12} md={6}>
                <MKBox mb={{ xs: 5, md: 0 }}
                sx={{
                  p: 2, // smaller padding
                  width: "100%", // or set a fixed width like '300px'
                  maxWidth: "75%", // optional max width
                  backgroundColor: "#e3f2fd", // light blue background
                  border: "1px solid #0d3f8f", // blue border
                  borderRadius: 2,
                  transition: "all 0.3s ease",
                  "&:hover": {
                    boxShadow: 8,
                    backgroundColor: "#bbdefb", // slightly darker blue on hover
                  },
                }}
                >
                  <DefaultInfoCard
                    icon="gavel"
                    title="Ethical Trust"
                    description="Build trust with transparent, ethical technology."
                  />
                </MKBox>
              </Grid>
              <Grid item xs={12} md={6}>
                <MKBox mb={{ xs: 5, md: 0 }}
                sx={{
                  p: 2, // smaller padding
                  width: "100%", // or set a fixed width like '300px'
                  maxWidth: "75%", // optional max width
                  backgroundColor: "#e3f2fd", // light blue background
                  border: "1px solid #0d3f8f", // blue border
                  borderRadius: 2,
                  transition: "all 0.3s ease",
                  "&:hover": {
                    boxShadow: 8,
                    backgroundColor: "#bbdefb", // slightly darker blue on hover
                  },
                }}
                >
                  <DefaultInfoCard
                    icon="peopleIcon"
                    title="Community-driven"
                    description="Everyone can help making London a safer place."
                  />
                </MKBox>
              </Grid>
            </Grid>
          </Grid>
          {/*
          <Grid item xs={12} lg={4} sx={{ ml: "auto", mt: { xs: 3, lg: 0 } }}>
            <CenteredBlogCard
              image="https://images.unsplash.com/photo-1544717302-de2939b7ef71?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80"
              title="Get insights on Search"
              description="Website visitors today demand a frictionless user expericence — especially when using search. Because of the hight standards."
              action={{
                type: "internal",
                route: "pages/company/about-us",
                color: "info",
                label: "find out more",
              }}
            />
          </Grid>
          */}
        </Grid>
      </Container>
    </MKBox>
  );
}

export default Information;
