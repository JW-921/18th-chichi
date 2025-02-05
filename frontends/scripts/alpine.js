import Alpine from "alpinejs";
window.Alpine = Alpine;

function formHandler() {
  return {
    products: [{ name: "" }],
    options: [{ name: "", price: 0 }],
    activeSection: null,
    toggleSection(section) {
      this.activeSection = this.activeSection === section ? null : section;
    },
    addProduct() {
      this.products.push({ name: "" });
    },
    removeProduct(index) {
      this.products.splice(index, 1);
    },
    addOption() {
      this.options.push({ name: "", price: 0 });
    },
    removeOption(index) {
      this.options.splice(index, 1);
    },
    resetForm() {
      this.products = [{ name: "" }];
    },
    resetOptions() {
      this.options = [{ name: "", price: 0 }];
    },
  };
}
window.formHandler = formHandler;

function rewardForm(basePrice) {
  return {
    basePrice: parseFloat(basePrice),
    totalPrice: parseFloat(basePrice),
    updateTotal(event) {
      const price = parseFloat(event.target.dataset.price);
      if (event.target.checked) {
        this.totalPrice += price;
      } else {
        this.totalPrice -= price;
      }
    },
  };
}

window.rewardForm = rewardForm;

function fileUploadHandler() {
  return {
    fileName: "尚未選擇檔案",
    previewUrl: null,

    handleFile(event) {
      const file = event.target.files[0];

      if (file) {
        this.fileName = file.name;

        const reader = new FileReader();
        reader.onload = (e) => {
          this.previewUrl = e.target.result;
        };
        reader.readAsDataURL(file);
      } else {
        this.fileName = "尚未選擇檔案";
        this.previewUrl = null;
      }
    },
  };
}
window.fileUploadHandler = fileUploadHandler;

function initBackToTopButton() {
  return {
    isVisible: false, // 狀態控制按鈕是否顯示

    init() {
      // 監聽滾動事件
      window.addEventListener("scroll", () => {
        this.isVisible = window.scrollY > 300; // 滾動超過 300px 顯示按鈕
      });
    },

    scrollToTop() {
      // 平滑滾動到頁面頂部
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    },
  };
}
window.initBackToTopButton = initBackToTopButton;

function rewardManager() {
  return {
    showToast: false,
    toastMessage: "",
    validateBeforeAdd(event) {
      // 停止默認的鏈接跳轉行為
      event.preventDefault();

      // 檢查是否存在商品
      const hasProducts = document.querySelectorAll("#product-list li:not(.text-gray-500)").length > 0;

      if (!hasProducts) {
        this.toastMessage = "請先新增商品，再新增回饋方案！";
        this.showToast = true;

        // 1.5 秒後自動隱藏提示框
        setTimeout(() => {
          this.showToast = false;
        }, 1500);
      } else {
        // 從按鈕的 href 屬性獲取目標 URL
        const targetUrl = event.target.closest("a").getAttribute("href");
        window.location.href = targetUrl;
      }
    },
  };
}
window.rewardManager = rewardManager;

function dateValidationHandler(defaultDate, today) {
  return {
    selectedDate: defaultDate || "", // 初始化為預設值或空字串
    isInvalid: false,
    today: today,

    validateDate() {
      // 檢查日期是否有效
      this.isInvalid = this.selectedDate > this.today;
    },

    init() {
      // 預設值初始化時進行驗證
      if (this.selectedDate) {
        this.validateDate();
      }
    },
  };
}
window.dateValidationHandler = dateValidationHandler;

function goalAmountHandler(defaultAmount = 0) {
  defaultAmount = parseInt(defaultAmount, 10) || 0; // 確保 defaultAmount 為有效數字
  return {
    goalAmountRaw: defaultAmount > 0 ? defaultAmount.toString() : "", // 預設輸入值

    validateInput(event) {
      // 移除非數字字符
      const input = event.target.value.replace(/[^0-9]/g, "");
      const parsedValue = parseInt(input, 10);

      // 檢查範圍並更新值
      if (isNaN(parsedValue) || parsedValue < 1) {
        this.goalAmountRaw = ""; // 清空輸入框值
      } else if (parsedValue > 9999999999) {
        this.goalAmountRaw = parsedValue.toString().slice(0, 10); // 限制 10 位數
      } else {
        this.goalAmountRaw = input; // 更新原始輸入值
      }
    },
  };
}
window.goalAmountHandler = goalAmountHandler;

function categoryManager() {
  return {
    activeTab: document.querySelector("[data-current-category]")?.dataset?.currentCategory || "全部",
    scrollContainer: null,
    showLeftArrow: false,
    showRightArrow: false,
    init() {
      this.scrollContainer = document.querySelector("[data-category-nav]");
      if (!this.scrollContainer) {
        console.error("Scroll container not found!");
        return;
      }

      this.checkArrows();
      this.scrollContainer.addEventListener("scroll", () => this.checkArrows());

      // 頁面載入後自動捲動到當前 activeTab 按鈕
      window.addEventListener("DOMContentLoaded", () => {
        const activeBtn = this.scrollContainer.querySelector(`[data-category='${this.activeTab}']`);
        if (activeBtn) {
          activeBtn.scrollIntoView({
            behavior: "smooth",
            inline: "center",
          });
        } else {
          console.warn("Active button not found!");
        }
      });
    },
    checkArrows() {
      if (!this.scrollContainer) return;
      this.showLeftArrow = this.scrollContainer.scrollLeft > 0;
      this.showRightArrow = this.scrollContainer.scrollLeft < this.scrollContainer.scrollWidth - this.scrollContainer.clientWidth;

      this.updateArrowsVisibility();
    },
    updateArrowsVisibility() {
      const leftArrow = document.querySelector("[data-left-arrow]");
      const rightArrow = document.querySelector("[data-right-arrow]");
      if (leftArrow) leftArrow.style.display = this.showLeftArrow ? "flex" : "none";
      if (rightArrow) rightArrow.style.display = this.showRightArrow ? "flex" : "none";
    },
    scrollLeft() {
      if (this.scrollContainer) this.scrollContainer.scrollBy({ left: -400, behavior: "smooth" });
    },
    scrollRight() {
      if (this.scrollContainer) this.scrollContainer.scrollBy({ left: 400, behavior: "smooth" });
    },
    filterProjects(category) {
      this.activeTab = category;
      const url = new URL(window.location.href);
      url.search = "";
      if (category !== "全部") {
        url.searchParams.set("category", category);
      }
      window.location.href = url.toString();
    },
  };
}

window.categoryManager = categoryManager;

function categoryManagerall() {
  return {
    activeTab: document.querySelector("[data-current-category]")?.dataset?.currentCategory || "全部",
    scrollContainer: null,
    showLeftArrow: false,
    showRightArrow: false,
    init() {
      this.scrollContainer = document.querySelector("[data-category-nav]");
      if (!this.scrollContainer) {
        console.error("Scroll container not found!");
        return;
      }

      this.checkArrows();
      this.scrollContainer.addEventListener("scroll", () => this.checkArrows());

      const activeBtn = this.scrollContainer.querySelector(`[data-category='${this.activeTab}']`);
      if (activeBtn) {
        activeBtn.scrollIntoView({
          behavior: "smooth",
          inline: "center",
        });
      }
    },
    checkArrows() {
      if (!this.scrollContainer) return;
      this.showLeftArrow = this.scrollContainer.scrollLeft > 0;
      this.showRightArrow = this.scrollContainer.scrollLeft < this.scrollContainer.scrollWidth - this.scrollContainer.clientWidth;

      this.updateArrowsVisibility();
    },
    updateArrowsVisibility() {
      const leftArrow = document.querySelector("[data-left-arrow]");
      const rightArrow = document.querySelector("[data-right-arrow]");

      if (leftArrow) leftArrow.style.display = this.showLeftArrow ? "flex" : "none";
      if (rightArrow) rightArrow.style.display = this.showRightArrow ? "flex" : "none";
    },
    scrollLeft() {
      if (this.scrollContainer) this.scrollContainer.scrollBy({ left: -400, behavior: "smooth" });
    },
    scrollRight() {
      if (this.scrollContainer) this.scrollContainer.scrollBy({ left: 400, behavior: "smooth" });
    },
    filterProjects(category) {
      this.activeTab = category;
      const url = new URL(window.location.href);
      url.search = "";
      if (category !== "全部") {
        url.searchParams.set("category", category);
      }
      window.location.href = url.toString();
    },
  };
}

window.categoryManagerall = categoryManagerall;
