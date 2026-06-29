// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-projects",
          title: "projects",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-repositories",
          title: "repositories",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/repositories/";
          },
        },{id: "nav-teaching",
          title: "teaching",
          description: "Teaching, tutoring, and mentoring in statistics and quantitative methods.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/teaching/";
          },
        },{id: "news-a-simple-inline-announcement",
          title: 'A simple inline announcement.',
          description: "",
          section: "News",},{id: "news-a-long-announcement-with-details",
          title: 'A long announcement with details',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/announcement_2/";
            },},{id: "news-a-simple-inline-announcement-with-markdown-emoji-sparkles-smile",
          title: 'A simple inline announcement with Markdown emoji! :sparkles: :smile:',
          description: "",
          section: "News",},{id: "projects-reproducing-a-published-air-quality-model",
          title: 'Reproducing a Published Air-Quality Model',
          description: "A reproducibility audit of a peer-reviewed benzene-estimation study — rebuilding its results from the data and methods alone to see what holds up",
          section: "Projects",handler: () => {
              window.location.href = "/projects/air_quality_reproducibility/";
            },},{id: "projects-does-studying-more-raise-gpa-a-causal-inference-workflow",
          title: 'Does Studying More Raise GPA? A Causal-Inference Workflow',
          description: "A plain regression says studying lowers GPA. Here&#39;s why that&#39;s wrong, and how matching gets closer to the real answer.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/causal_study_gpa/";
            },},{id: "projects-e-commerce-customer-segmentation-sql",
          title: 'E-commerce Customer Segmentation (SQL)',
          description: "RFM segmentation of 93K customers across 99K real orders — Python ETL into SQLite, SQL window-function scoring, and a clear answer to where the revenue sits",
          section: "Projects",handler: () => {
              window.location.href = "/projects/ecommerce_rfm/";
            },},{id: "projects-seattle-king-county-housing-analytics",
          title: 'Seattle / King County Housing Analytics',
          description: "Multi-source analysis of 271K property sales — price trends, school &amp; waterfront premiums, and XGBoost hedonic pricing model",
          section: "Projects",handler: () => {
              window.location.href = "/projects/housing_analytics/";
            },},{id: "projects-retail-operations-dashboard-power-bi",
          title: 'Retail Operations Dashboard (Power BI)',
          description: "End-to-end Power BI analytics for a fictional specialty retail chain — semantic model design, 18 custom DAX measures, and two interactive dashboards covering executive KPIs and labor efficiency",
          section: "Projects",handler: () => {
              window.location.href = "/projects/retail_dashboard/";
            },},{id: "projects-predicting-sepsis-from-patient-vitals",
          title: 'Predicting Sepsis from Patient Vitals',
          description: "A clinical risk model on severely imbalanced patient data — why accuracy lies, and how class-weighting plus the right metric surface the cases that matter",
          section: "Projects",handler: () => {
              window.location.href = "/projects/sepsis_prediction/";
            },},{
        id: 'social-cv',
        title: 'CV',
        section: 'Socials',
        handler: () => {
          window.open("/assets/pdf/Yijia-Wang_Data-Scientist-Resume_26-04-21.pdf", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/yijiaw0725", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/yijiawang725", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
