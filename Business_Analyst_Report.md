# Business Report: Tech Request System Automation

**Date:** May 16, 2025
**Author:** Ram Sharma

## 1. Overview

In this report, I detail the automation of the internal tech solution request process. The previous manual email system I observed was slow and difficult to track. The new system I've developed uses a web form for requests, emails for approvals, and logs everything in Excel. I believe this will make things faster, clearer, and easier to manage.

## 2. The Problem

The old way of handling tech requests by email had several issues identified:

*   **Slow:** Requests often got lost or delayed.
*   **Confusing:** It was hard to determine priorities.
*   **Not Clear:** People asking for help didn't know their request status.
*   **Extra Work:** A lot of time was spent manually tracking and updating.

## 3. The Solution: Automated System

I've built an automated system with the following components:

1.  **Web Form:** A modern, easy-to-use online form I designed for submitting requests.
2.  **Email Approvals:** The IT Manager now receives an email with "Approve" or "Reject" links for quick decisions.
3.  **Notifications:** Users get emails confirming their request and its final status, a feature I implemented for transparency.
4.  **Excel Logging:** Approved requests are saved in an Excel file (`requests.xlsx`) where I've included auto-sized columns for readability.
5.  **Activity Log:** I've added a log file (`app.log`) to track system actions, which will be helpful for troubleshooting.

## 4. How It Works (Simplified)

Here’s a simplified flow of the system I designed:

1.  A user fills out the web form.
2.  The system emails the IT Manager for approval.
3.  The user gets a confirmation email.
4.  The IT Manager approves/rejects via the email link.
5.  If approved, the details go into `requests.xlsx`.
6.  The user gets a final status update email.

## 5. Key Benefits

I expect this system to deliver several key benefits:

*   **Faster Turnaround:** Quicker processing of requests.
*   **Clearer Process:** Everyone involved will know the status of requests.
*   **Less Manual Work:** This should free up IT staff time significantly.
*   **Better Tracking:** It will be easy to see all approved projects.

## 6. Potential Risks

I've identified a few potential risks to consider:

*   **Email Issues:** Emails might go to spam. I'll need to ensure SMTP settings are correct and perhaps advise on whitelisting.
*   **Excel Limits:** For very high volume, Excel might not be the ideal long-term solution. I might consider a database in the future.
*   **User Adoption:** I'll need to ensure users are comfortable with the new form and process.

## 7. Future Ideas

Looking ahead, I have some ideas for future enhancements:

*   A dashboard for the IT Manager to see all requests at a glance.
*   Migrating from Excel to a database for more robust data management.
*   Developing more detailed reports and analytics from the request data.

## 8. Conclusion

I believe this new automated system is a significant improvement over the old manual process. It should make requesting and managing tech solutions much smoother and more efficient. I've designed it to be user-friendly and it provides a solid base for future improvements I might undertake.