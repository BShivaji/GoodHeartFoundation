document.addEventListener("DOMContentLoaded", () => {
    const title = document.querySelector("[data-admin-title]");
    if (title) {
        title.dataset.loaded = "true";
    }

    const logoutLink = document.querySelector("[data-logout-link]");
    if (logoutLink) {
        logoutLink.addEventListener("click", (event) => {
            const shouldLogout = window.confirm(
                "Are you sure you want to log out and return to the home page?"
            );

            if (!shouldLogout) {
                event.preventDefault();
            }
        });
    }

    const searchInput = document.querySelector("[data-volunteer-search]");
    const volunteerCards = document.querySelectorAll("[data-volunteer-card]");
    const emptyState = document.querySelector("[data-volunteer-empty]");

    if (searchInput && volunteerCards.length) {
        searchInput.addEventListener("input", () => {
            const query = searchInput.value.trim().toLowerCase();
            let visibleCount = 0;

            volunteerCards.forEach((card) => {
                const haystack = card.dataset.search || "";
                const matches = !query || haystack.includes(query);
                card.hidden = !matches;

                if (matches) {
                    visibleCount += 1;
                }
            });

            if (emptyState) {
                emptyState.hidden = visibleCount !== 0;
            }
        });
    }

    const eventModal = document.querySelector("[data-event-modal]");
    const openEventModalButton = document.querySelector("[data-open-event-modal]");
    const closeEventModalButtons = document.querySelectorAll("[data-close-event-modal]");

    if (eventModal && openEventModalButton) {
        const openModal = () => {
            eventModal.hidden = false;
            document.body.style.overflow = "hidden";
            const firstInput = eventModal.querySelector("input, textarea");
            if (firstInput) {
                firstInput.focus();
            }
        };

        const closeModal = () => {
            eventModal.hidden = true;
            document.body.style.overflow = "";
        };

        openEventModalButton.addEventListener("click", openModal);

        closeEventModalButtons.forEach((button) => {
            button.addEventListener("click", closeModal);
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && !eventModal.hidden) {
                closeModal();
            }
        });
    }

    const eventDetailModal = document.querySelector("[data-event-details-modal]");
    const eventCards = document.querySelectorAll("[data-event-card-open]");
    const closeEventDetailButtons = document.querySelectorAll("[data-close-event-details-modal]");
    const eventDetailTitle = document.querySelector("[data-event-details-title]");
    const eventDetailStatus = document.querySelector("[data-event-details-status]");
    const eventDetailLocation = document.querySelector("[data-event-details-location]");
    const eventDetailDescription = document.querySelector("[data-event-details-description]");
    const eventDateInput = document.querySelector("[data-event-details-modal] #event-details-date");
    const eventDateForm = document.querySelector("[data-event-date-form]");
    const eventDeleteButton = document.querySelector("[data-event-delete-button]");

    if (eventDetailModal && eventCards.length) {
        const openEventDetailModal = (card) => {
            if (eventDetailTitle) {
                eventDetailTitle.textContent = card.dataset.eventTitle || "Event";
            }
            if (eventDetailStatus) {
                eventDetailStatus.textContent = card.dataset.eventStatus || "Unknown";
            }
            if (eventDetailLocation) {
                eventDetailLocation.textContent = card.dataset.eventLocation || "-";
            }
            if (eventDetailDescription) {
                eventDetailDescription.textContent = card.dataset.eventDescription || "-";
            }
            if (eventDateInput) {
                eventDateInput.value = card.dataset.eventDate || "";
            }
            if (eventDateForm) {
                eventDateForm.action = `/admin/events/${card.dataset.eventId}/update-date`;
            }
            if (eventDeleteButton) {
                eventDeleteButton.setAttribute("formaction", `/admin/events/${card.dataset.eventId}/delete`);
            }

            eventDetailModal.hidden = false;
            document.body.style.overflow = "hidden";
        };

        const closeEventDetailModal = () => {
            eventDetailModal.hidden = true;
            document.body.style.overflow = "";
        };

        eventCards.forEach((card) => {
            card.addEventListener("click", () => openEventDetailModal(card));
        });

        closeEventDetailButtons.forEach((button) => {
            button.addEventListener("click", closeEventDetailModal);
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && !eventDetailModal.hidden) {
                closeEventDetailModal();
            }
        });
    }

    const donorModal = document.querySelector("[data-donor-modal]");
    const openDonorModalButton = document.querySelector("[data-open-donor-modal]");
    const closeDonorModalButtons = document.querySelectorAll("[data-close-donor-modal]");
    const openDonorEditButtons = document.querySelectorAll("[data-open-donor-edit]");
    const donorForm = document.querySelector("[data-donor-form]");
    const donorDeleteButton = document.querySelector("[data-donor-delete-button]");
    const donorModalTitle = document.querySelector("[data-donor-modal-title]");
    const donorModalEyebrow = document.querySelector("[data-donor-modal-eyebrow]");
    const donorSubmitButton = document.querySelector("[data-donor-submit-button]");
    const donorNameInput = document.querySelector("#donor-name");
    const donorDateInput = document.querySelector("#donation-date");
    const donorAmountInput = document.querySelector("#donor-amount");
    const donorPurposeInput = document.querySelector("#donor-purpose");

    if (donorModal && donorForm) {
        const openDonorModal = () => {
            donorModal.hidden = false;
            document.body.style.overflow = "hidden";
            const firstInput = donorModal.querySelector("input, textarea");
            if (firstInput) {
                firstInput.focus();
            }
        };

        const closeDonorModal = () => {
            donorModal.hidden = true;
            document.body.style.overflow = "";
        };

        const setDonorCreateMode = () => {
            donorForm.action = "/admin/add-donor";
            if (donorDeleteButton) {
                donorDeleteButton.hidden = true;
                donorDeleteButton.setAttribute("formaction", "");
            }
            if (donorModalTitle) {
                donorModalTitle.textContent = "Add Donor Details";
            }
            if (donorModalEyebrow) {
                donorModalEyebrow.textContent = "Add Donor";
            }
            if (donorSubmitButton) {
                donorSubmitButton.textContent = "Save Donor";
            }
            if (donorNameInput) donorNameInput.value = "";
            if (donorDateInput) donorDateInput.value = "";
            if (donorAmountInput) donorAmountInput.value = "";
            if (donorPurposeInput) donorPurposeInput.value = "";
        };

        const setDonorEditMode = (button) => {
            const fundId = button.dataset.fundId;
            donorForm.action = `/admin/funds/${fundId}/update`;
            if (donorDeleteButton) {
                donorDeleteButton.hidden = false;
                donorDeleteButton.setAttribute("formaction", `/admin/funds/${fundId}/delete`);
            }
            if (donorModalTitle) {
                donorModalTitle.textContent = "Modify Donor Details";
            }
            if (donorModalEyebrow) {
                donorModalEyebrow.textContent = "Edit Donor";
            }
            if (donorSubmitButton) {
                donorSubmitButton.textContent = "Update Donor";
            }
            if (donorNameInput) donorNameInput.value = button.dataset.donorName || "";
            if (donorDateInput) donorDateInput.value = button.dataset.donationDate || "";
            if (donorAmountInput) donorAmountInput.value = button.dataset.amount || "";
            if (donorPurposeInput) donorPurposeInput.value = button.dataset.purpose || "";
        };

        if (openDonorModalButton) {
            openDonorModalButton.addEventListener("click", () => {
                setDonorCreateMode();
                openDonorModal();
            });
        }

        openDonorEditButtons.forEach((button) => {
            button.addEventListener("click", () => {
                setDonorEditMode(button);
                openDonorModal();
            });
        });

        closeDonorModalButtons.forEach((button) => {
            button.addEventListener("click", closeDonorModal);
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && !donorModal.hidden) {
                closeDonorModal();
            }
        });
    }

    const expenditureModal = document.querySelector("[data-expenditure-modal]");
    const openExpenditureModalButton = document.querySelector("[data-open-expenditure-modal]");
    const closeExpenditureModalButtons = document.querySelectorAll("[data-close-expenditure-modal]");
    const openExpenditureEditButtons = document.querySelectorAll("[data-open-expenditure-edit]");
    const expenditureForm = document.querySelector("[data-expenditure-form]");
    const expenditureDeleteButton = document.querySelector("[data-expenditure-delete-button]");
    const expenditureTitle = document.querySelector("[data-expenditure-modal-title]");
    const expenditureEyebrow = document.querySelector("[data-expenditure-modal-eyebrow]");
    const expenditureSubmitButton = document.querySelector("[data-expenditure-submit-button]");
    const expenditureEventName = document.querySelector("#expense-event-name");
    const expenditureDate = document.querySelector("#expense-date");
    const expenditureAmount = document.querySelector("#expense-amount");
    const expenditurePurpose = document.querySelector("#expense-purpose");

    if (expenditureModal && expenditureForm) {
        const openExpenditureModal = () => {
            expenditureModal.hidden = false;
            document.body.style.overflow = "hidden";
        };

        const closeExpenditureModal = () => {
            expenditureModal.hidden = true;
            document.body.style.overflow = "";
        };

        const setCreateMode = () => {
            expenditureForm.action = "/admin/add-expenditure";
            if (expenditureDeleteButton) {
                expenditureDeleteButton.hidden = true;
                expenditureDeleteButton.setAttribute("formaction", "");
            }
            if (expenditureTitle) {
                expenditureTitle.textContent = "Add Expenditure Details";
            }
            if (expenditureEyebrow) {
                expenditureEyebrow.textContent = "Add Expenditure";
            }
            if (expenditureSubmitButton) {
                expenditureSubmitButton.textContent = "Save Expenditure";
            }
            if (expenditureEventName) {
                expenditureEventName.value = "";
            }
            if (expenditureDate) {
                expenditureDate.value = "";
            }
            if (expenditureAmount) {
                expenditureAmount.value = "";
            }
            if (expenditurePurpose) {
                expenditurePurpose.value = "";
            }
        };

        const setEditMode = (button) => {
            const expenditureId = button.dataset.expenditureId;
            expenditureForm.action = `/admin/expenditures/${expenditureId}/update`;
            if (expenditureDeleteButton) {
                expenditureDeleteButton.hidden = false;
                expenditureDeleteButton.setAttribute("formaction", `/admin/expenditures/${expenditureId}/delete`);
            }
            if (expenditureTitle) {
                expenditureTitle.textContent = "Modify Expenditure";
            }
            if (expenditureEyebrow) {
                expenditureEyebrow.textContent = "Edit Expenditure";
            }
            if (expenditureSubmitButton) {
                expenditureSubmitButton.textContent = "Update Expenditure";
            }
            if (expenditureEventName) {
                expenditureEventName.value = button.dataset.eventName || "";
            }
            if (expenditureDate) {
                expenditureDate.value = button.dataset.expenseDate || "";
            }
            if (expenditureAmount) {
                expenditureAmount.value = button.dataset.amount || "";
            }
            if (expenditurePurpose) {
                expenditurePurpose.value = button.dataset.purpose || "";
            }
        };

        if (openExpenditureModalButton) {
            openExpenditureModalButton.addEventListener("click", () => {
                setCreateMode();
                openExpenditureModal();
            });
        }

        openExpenditureEditButtons.forEach((button) => {
            button.addEventListener("click", () => {
                setEditMode(button);
                openExpenditureModal();
            });
        });

        closeExpenditureModalButtons.forEach((button) => {
            button.addEventListener("click", closeExpenditureModal);
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && !expenditureModal.hidden) {
                closeExpenditureModal();
            }
        });
    }

    const recentWorkModal = document.querySelector("[data-recent-work-modal]");
    const openRecentWorkModalButton = document.querySelector("[data-open-recent-work-modal]");
    const closeRecentWorkModalButtons = document.querySelectorAll("[data-close-recent-work-modal]");

    if (recentWorkModal && openRecentWorkModalButton) {
        const openRecentWorkModal = () => {
            recentWorkModal.hidden = false;
            document.body.style.overflow = "hidden";
            const firstInput = recentWorkModal.querySelector("input, textarea");
            if (firstInput) {
                firstInput.focus();
            }
        };

        const closeRecentWorkModal = () => {
            recentWorkModal.hidden = true;
            document.body.style.overflow = "";
        };

        openRecentWorkModalButton.addEventListener("click", openRecentWorkModal);

        closeRecentWorkModalButtons.forEach((button) => {
            button.addEventListener("click", closeRecentWorkModal);
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && !recentWorkModal.hidden) {
                closeRecentWorkModal();
            }
        });
    }

    // Apply template-driven visual values (data attributes -> inline styles)
    const applyFillWidths = () => {
        const fills = document.querySelectorAll('[data-fill-width]');
        fills.forEach((el) => {
            const v = el.getAttribute('data-fill-width');
            if (v !== null && v !== '') {
                el.style.width = String(v).trim() + '%';
            }
        });
    };

    const applySwatches = () => {
        const swatches = document.querySelectorAll('[data-swatch-color]');
        swatches.forEach((el) => {
            const c = el.getAttribute('data-swatch-color') || '';
            if (c) {
                el.style.backgroundColor = c;
                el.style.borderColor = c;
            }
        });
    };

    const applyBarHeights = () => {
        const bars = document.querySelectorAll('[data-bar-height]');
        bars.forEach((el) => {
            const h = el.getAttribute('data-bar-height');
            if (h !== null && h !== '') {
                el.style.height = String(h).trim() + 'px';
            }
        });
    };

    applyFillWidths();
    applySwatches();
    applyBarHeights();
});
