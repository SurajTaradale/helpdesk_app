import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
const menuData = [
  {
    title: 'Dashboard',
    icon: <HomeIcon />,
    path: '/agent/dashboard',
    // children: [
    //   {
    //     title: 'Important',
    //     path: '/inbox/important',
    //     icon: 'MailIcon',
    //   },
    //   {
    //     title: 'Sent Items',
    //     path: '/inbox/sent',
    //     icon: 'MailIcon',
    //   },
    // ],
  },
  {
    title: 'Admin',
    icon: <InfoIcon />,
    path: '/agent/admin',
  },
];

export default menuData;
