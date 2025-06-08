// @mui icons
//import FacebookIcon from "@mui/icons-material/Facebook";
//import TwitterIcon from "@mui/icons-material/Twitter";
//import GitHubIcon from "@mui/icons-material/GitHub";
//import YouTubeIcon from "@mui/icons-material/YouTube";

// Material Kit 2 React components
import MKTypography from "components/MKTypography";

// Images
import logoCT from "assets/images/newlogo1.png";

const date = new Date().getFullYear();

export default {
  brand: {
    name: "StreetGuard",
    image: logoCT,
    route: "/",
  },
  socials: [],
  menus: [
    {
      name: "company",
      items: [
        { name: "about us", href: "/pages/landing-pages/about-us" },
      ],
    },
    {
      name: "Tool Access",
      items: [
        { name: "sign in", href: "/pages/authentication/sign-in" },]
    },
    {
      name: "help & support",
      items: [
        { name: "contact us", href: "/pages/landing-pages/contact-us" },
      ],
    },
    {
      name: "legal",
      items: [
        { name: "terms & conditions", href: "/pages/landing-pages/terms" },
        { name: "privacy policy", href: "/pages/landing-pages/policy" },
      ],
    },
  ],
  copyright: (
    <MKTypography variant="button" fontWeight="regular">
      All rights reserved. Copyright &copy; {date} StreetGuard
      <MKTypography
        component="a"
        target="_blank"
        rel="noreferrer"
        variant="button"
        fontWeight="regular"
      >
      </MKTypography>
      .
    </MKTypography>
  ),
};
