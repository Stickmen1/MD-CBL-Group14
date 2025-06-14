// @mui material components
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";

// Material Kit 2 React components
import MKBox from "components/MKBox";

// Material Kit 2 React examples
//import DefaultCounterCard from "examples/Cards/CounterCards/DefaultCounterCard";

// Images
import police from "assets/images/logos/gray-logos/svg.svg";
//import coinbase from "assets/images/logos/gray-logos/logo-coinbase.svg";
import nasa from "assets/images/logos/gray-logos/City_of_London_logo.svg";
import netflix from "assets/images/logos/gray-logos/Mayor_of_London_logo1.svg";
import pinterest from "assets/images/logos/gray-logos/logo.svg";
import spotify from "assets/images/logos/gray-logos/logo1.svg";
//import vodafone from "assets/images/logos/gray-logos/logo-vodafone.svg";

function Featuring() {
  return (
    <MKBox component="section" pt={5} pb={1}>
      <Container>
        <Grid container spacing={3} sx={{ mb: 1 }}>
          <Grid item xs={2.4} md={2.4} lg={2.4}>
            <MKBox component="img" src={police} alt="police" width="100%" opacity={0.7} objectFit='contain' height='100px'/>
          </Grid>
          <Grid item xs={2.4} md={2.4} lg={2.4}>
            <MKBox component="img" src={nasa} alt="nasa" width="100%" opacity={0.7} objectFit='contain' height='100px'/>
          </Grid>
          <Grid item xs={2.4} md={2.4} lg={2.4}>
            <MKBox component="img" src={netflix} alt="netflix" width="100%" opacity={0.7} objectFit='contain' height='100px'/>
          </Grid>
          <Grid item xs={2.4} md={2.4} lg={2.4}>
            <MKBox component="img" src={pinterest} alt="pinterest" width="100%" opacity={0.7} objectFit='contain' height='100px'/>
          </Grid>
          <Grid item xs={2.4} md={2.4} lg={2.4}>
            <MKBox component="img" src={spotify} alt="spotify" width="100%" opacity={0.7} objectFit='contain' height='100px'/>
          </Grid>
        </Grid>
        {/*
        <Grid container justifyContent="center" sx={{ textAlign: "center" }}>
          <Grid item xs={12} md={3}>
            <DefaultCounterCard
              count={5234}
              separator=","
              title="Projects"
              description="Of “high-performing” level are led by a certified project manager"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <DefaultCounterCard
              count={3400}
              separator=","
              suffix="+"
              title="Hours"
              description="That meets quality standards required by our users"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <DefaultCounterCard
              count={24}
              suffix="/7"
              title="Support"
              description="Actively engage team members that finishes on time"
            />
          </Grid>
        </Grid>
        */}
      </Container>
    </MKBox>
  );
}

export default Featuring;
