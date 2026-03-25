package com.diabetesapp.dto;

import com.diabetesapp.model.GlucoseRecord;
import jakarta.validation.constraints.*;
import lombok.Data;
import java.time.LocalDateTime;

public class GlucoseRecordDto {

    /**Create/Update */
    @Data
    public static class Request {
        @NotNull
        @Min(10) @Max(600)
        private Integer value;

        private LocalDateTime recordedAt;

        private GlucoseRecord.MealContext mealContext;

        @Size(max = 500)
        private String note;
    }

    /**API response */
    @Data
    public static class Response {
        private Long id;
        private Integer value;
        private LocalDateTime recordedAt;
        private GlucoseRecord.MealContext mealContext;
        private String note;
        private GlucoseRecord.GlucoseStatus status;

        public static Response from(GlucoseRecord r) {
            Response dto = new Response();
            dto.setId(r.getId());
            dto.setValue(r.getValue());
            dto.setRecordedAt(r.getRecordedAt());
            dto.setMealContext(r.getMealContext());
            dto.setNote(r.getNote());
            dto.setStatus(r.getStatus());
            return dto;
        }
    }

    /**Dashboard Summary Stats */
    @Data
    public static class Stats {
        private Double todayAvg;
        private Double weekAvg;
        private Integer totalReadings;
        private Integer inRangeCount;
        private Double inRangePercent;
        private Double currentA1cEstimate;
    }
}
