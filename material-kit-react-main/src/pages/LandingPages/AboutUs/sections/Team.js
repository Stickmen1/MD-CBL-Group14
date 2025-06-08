// @mui material components
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";

// Material Kit 2 React components
import MKBox from "components/MKBox";
import MKTypography from "components/MKTypography";

// Material Kit 2 React examples
import HorizontalTeamCard from "examples/Cards/TeamCards/HorizontalTeamCard";

// Images
//import team1 from "assets/images/team-5.jpg";
//import team2 from "assets/images/bruce-mars.jpg";
//import team3 from "assets/images/ivana-squares.jpg";
//import team4 from "assets/images/ivana-square.jpg";
import team5 from "assets/images/bg-about-us.jpg";

function Team() {
  return (
    <MKBox
      component="section"
      variant="gradient"
      bgColor="dark"
      position="relative"
      py={6}
      px={{ xs: 2, lg: 0 }}
      mx={-2}
    >
      <Container>
        <Grid container>
          <Grid item xs={12} md={8} sx={{ mb: 6 }}>
            <MKTypography variant="h3" color="white">
              Our Team
            </MKTypography>
            <MKTypography variant="body2" color="white" opacity={0.8}>
              Safety is our first concern, not deadlines. Nothing will happen until everything is 
              ready and we&apos;re absolutely confident. This will be a safe operation.
            </MKTypography>
          </Grid>
        </Grid>
        <Grid container spacing={3}>
          <Grid item xs={12} lg={6}>
            <MKBox mb={1}>
              <HorizontalTeamCard
                image={team5}
                name="Renée van den Bergen"
                position={{ color: "info", label: "Psychology and Technology" }}
                description="Expert in researching, gathering, analyzing, and synthesizing information."
              />
            </MKBox>
          </Grid>
          <Grid item xs={12} lg={6}>
            <MKBox mb={1}>
              <HorizontalTeamCard
                image={team5}
                name="Sven Collins"
                position={{ color: "info", label: "Data Science" }}
                description="Specialist in data science model creation, possessing a deep understanding of statistical methodologies."
              />
            </MKBox>
          </Grid>
          <Grid item xs={12} lg={6}>
            <MKBox mb={{ xs: 1, lg: 0 }}>
              <HorizontalTeamCard
                image={team5}
                name="Bálint Kecskeméti"
                position={{ color: "info", label: "Computer Science" }}
                description="Creation of graphs and producing files with practical value, possessing ability to analyze complex data sets."
              />
            </MKBox>
          </Grid>
          <Grid item xs={12} lg={6}>
            <MKBox mb={{ xs: 1, lg: 0 }}>
              <HorizontalTeamCard
                image={team5}
                name="Joris Lesterhuis"
                position={{ color: "info", label: "Data Science" }}
                description="Extensive expertise in developing data science models, having comprehensive grasp of statistical methods."
              />
            </MKBox>
          </Grid>
          <Grid item xs={12} lg={6}>
            <MKBox mb={{ xs: 1, lg: 0 }}>
              <HorizontalTeamCard
                image={team5}
                name="Momchil Milushev"
                position={{ color: "info", label: "Computer Science" }}
                description="Extensive experience in designing appealing web interfaces and ensuring integration of the tool."
              />
            </MKBox>
          </Grid>
          <Grid item xs={12} lg={6}>
            <MKBox mb={{ xs: 1, lg: 0 }}>
              <HorizontalTeamCard
                image={team5}
                name="Aleksandra Nowińska"
                position={{ color: "info", label: "Data Science" }}
                description="Designing and deploying robust predictive models that drive insights and support strategic decision-making."
              />
            </MKBox>
          </Grid>
        </Grid>
      </Container>
    </MKBox>
  );
}

export default Team;
