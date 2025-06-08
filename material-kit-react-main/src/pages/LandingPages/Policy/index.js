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

function Policy() {
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
                Privacy Policy
            </MKTypography>
        </MKBox>
        <MKBox display="flex" justifyContent="center" alignItems="center" minHeight="50vh" px={4} pt={4}>
          <MKTypography variant="body1" textAlign="justify" maxWidth="800px">
            Effective Date: 08.06.2025 <br />
            Website: https://streetguard.info <br />
            Location: Netherlands <br />
            StreetGuard (&quot;we&quot;, &quot;us&quot;, or &quot;our&quot;) respects your privacy and is committed to protecting the personal information you share with us.
            This Privacy Policy outlines how we collect, use, and protect your personal data when you access our website and services. <br /><br />
            
            1. Who We Are <br />
            StreetGuard provides a scheduling tool for patrol routes based on predictive models, intended for authorized law enforcement personnel in London.
            Access to the platform is managed internally by administrators, and not open to the general public. <br /><br />
            
            2. What Information We Collect <br />
            We collect and process the following types of personal data: <br />
            - Account Information <br />
            - Email address <br />
            - Password (stored securely using industry-standard encryption) <br />
            - Communication Data <br />
            - Messages submitted through our contact form <br />
            We do not collect sensitive personal data (e.g., race, health data) or financial data. <br /><br />
            
            3. How We Use Your Information <br />
            We use your personal data for the following purposes: <br />
            - To manage access to our services and ensure secure login <br />
            - To communicate with authorized users <br />
            - To respond to messages or inquiries sent via the contact form <br />
            - To improve our internal tools and services <br />
            We do not use your data for marketing or advertising purposes. <br /><br />
            
            4. Legal Basis for Processing <br />
            We process your data under the following legal bases: <br />
            - Consent: When you submit a message via our contact form <br />
            - Legitimate Interest: For secure access management and internal communication <br />
            - Legal Obligation: To comply with applicable Dutch and EU laws <br /><br />
            
            5. Data Sharing and Disclosure <br />
            We do not sell, rent, or trade your personal data. Your data may be shared only with: <br />
            - Authorized administrators for system and user access management <br />
            - Service providers (e.g., secure cloud storage, authentication platforms) who are contractually bound to GDPR compliance <br />
            We may disclose personal data if required by law or legal process. <br /><br />
            
            6. Data Storage and Security <br />
            We implement appropriate technical and organizational measures to protect your personal data, including: <br />
            - Encrypted storage of passwords <br />
            - Secure HTTPS connections <br />
            - Access controls and administrative oversight <br /><br />
            
            7. Data Retention <br />
            We retain your personal data only for as long as necessary: <br />
            - Account data: While your account is active or access is needed <br />
            - Contact form submissions: Up to 12 months after last communication, unless required longer for legal reasons. <br /><br />
            
            8. Your Rights (Under GDPR) <br />
            As a data subject, you have the right to: <br />
            - Access your personal data <br />
            - Rectify inaccuracies <br />
            - Request deletion (&ldquo;right to be forgotten&rdquo;) <br />
            - Restrict or object to processing <br />
            - Lodge a complaint with a supervisory authority (Autoriteit Persoonsgegevens in the Netherlands) <br />
            You may exercise your rights by contacting us (see Section 10). <br /><br />
            
            9. Third-Party Links <br />
            Our website does not include third-party ads or embedded content that collects your data.
            However, we may link to external sites (e.g., documentation or official pages). We are not responsible for their privacy practices. <br /><br />
            
            10. Contact Information <br />
            If you have any questions, concerns, or requests about this Privacy Policy or your data, please contact us at:
            Or use the contact form at: https://streetguard.info/pages/landing-pages/contact-us <br /><br />
            
            11. Changes to This Privacy Policy <br />
            We may update this Privacy Policy from time to time.
            When we do, we will update the &quot;Effective Date&quot; at the top and post a notice on our website.
            Continued use of our services after such changes constitutes your acknowledgment and agreement.
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

export default Policy;