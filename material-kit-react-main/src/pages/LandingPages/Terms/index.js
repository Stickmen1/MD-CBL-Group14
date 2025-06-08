// @mui material components
//import Card from "@mui/material/Card";

// Material Kit 2 React components
import MKBox from "components/MKBox";

// Material Kit 2 React examples
import DefaultNavbar from "examples/Navbars/DefaultNavbar";

// Author page sections
//import Profile from "pages/LandingPages/Author/sections/Profile";
//import Posts from "pages/LandingPages/Author/sections/Posts";
//import Contact from "pages/LandingPages/Author/sections/Contact";
import Footer from "pages/LandingPages/Author/sections/Footer";

// Routes
import routes from "routes";

// Images
import bgImage from "assets/images/city-profile.jpg";
import MKTypography from "components/MKTypography";

function Terms() {
  return (
    <>
      <MKBox position="fixed" top="0.5rem" width="100%">
        <DefaultNavbar
          routes={routes}
        />
      </MKBox>
      {/*
      <DefaultNavbar
        routes={routes}
        action={{
          type: "external",
          route: "",
          label: "free download",
          color: "info",
        }}
        transparent
        light
      />
      */}
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
            textAlign: "center",
            color: "white", // make text readable over dark overlay
            px: 2,
            }}
        >
            <MKTypography variant="h2" color="white" fontWeight="bold">
                Terms & Conditions
            </MKTypography>
        </MKBox>
        <MKBox display="flex" justifyContent="center" alignItems="center" minHeight="50vh" px={4} pt={4}>
            <MKTypography variant="body1" textAlign="justify" maxWidth="800px">
                Effective Date: 08.06.2025 <br />
                Welcome to StreetGuard. These Terms & Conditions (“Terms”) govern your access and use of the website 
                https://streetguard.info (the “Site”), operated by StreetGuard (“we”, “us”, or “our”), a company based in the Netherlands.
                By accessing or using this Site, you agree to be bound by these Terms. 
                If you do not agree with any part of these Terms, you may not use our Site. <br /><br />
                1. Use of the Website <br />
                Access to StreetGuard is restricted and managed by authorized administrators.
                Only designated personnel, such as members of approved law enforcement agencies, may use the scheduling tools and related features.
                You agree to use this Site only for lawful purposes and in accordance with these Terms. <br /><br />
                2. Access Credentials <br />
                Users are provided credentials (e.g., email and password) by the Site administrators.
                You are responsible for maintaining the confidentiality of any login information associated with your account.
                You must notify us immediately of any unauthorized use or security breach. <br /><br />
                3. Data Collection and Privacy <br />
                We collect basic personal data, including email addresses and passwords, to manage secure access. 
                We are committed to protecting your personal information and will outline our practices in a forthcoming Privacy Policy.
                Until then, your data will be handled responsibly and in accordance with applicable data protection laws in the Netherlands and the European Union. <br /><br />
                4. User Submissions <br />
                You may contact us or submit inquiries via the Contact Us page on our website. All messages and content sent through the Site become the property of StreetGuard. 
                We reserve the right to store, review, or use these submissions to improve our services or respond to inquiries. <br /><br />
                5. Intellectual Property
                All content on this Site, including but not limited to text, graphics, software, and layout, is the property of StreetGuard or its licensors and is protected by intellectual property laws. 
                Unauthorized reproduction or use of any content is strictly prohibited. <br /><br />
                6. No Warranties <br />
                StreetGuard is provided on an “as is” and “as available” basis. We do not guarantee the accuracy, completeness, or reliability of the Site or its tools. 
                We disclaim all warranties, express or implied, to the extent permitted by law. <br /><br />
                7. Limitation of Liability <br />
                To the maximum extent permitted by law, StreetGuard shall not be liable for any direct, indirect, incidental, or consequential damages resulting from your use of or inability to use the Site. <br /><br />
                8. Modifications to Terms <br />
                We reserve the right to update or modify these Terms at any time. If changes are made, we will post a notice on the Site. 
                Continued use of the Site after such modifications constitutes your acceptance of the revised Terms. <br /><br />
                9. Governing Law <br />
                These Terms are governed by and construed in accordance with the laws of the Netherlands, without regard to its conflict of law principles. <br /><br />
                10. Contact Information <br />
                For any questions about these Terms or the operation of this Site, please contact us at:
                https://streetguard.info/pages/landing-pages/contact-us
            </MKTypography>
        </MKBox>
        {/*}
        <Card
          sx={{
            p: 2,
            mx: { xs: 2, lg: 3 },
            mt: -8,
            mb: 4,
            backgroundColor: ({ palette: { white }, functions: { rgba } }) => rgba(white.main, 0.8),
            backdropFilter: "saturate(200%) blur(30px)",
            boxShadow: ({ boxShadows: { xxl } }) => xxl,
          }}
        >
          <Profile />
          <Posts />
        </Card>
        <Contact />
        */}
        <Footer />
      </MKBox>
    </>
  );
}

export default Terms;